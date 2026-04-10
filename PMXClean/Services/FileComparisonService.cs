namespace PMXClean.Services;

using System.Buffers;
using System.Collections.Concurrent;
using System.Collections.ObjectModel;
using System.IO;
using System.Text.Json;
using PMXClean.Models;

/// <summary>
/// Service for comparing Python and JSON files using LCS-based diff algorithm.
/// </summary>
public static class FileComparisonService
{
    private const string LockPattern = "#lock";

    /// <summary>
    /// Supported file extensions for comparison.
    /// </summary>
    private static readonly string[] SupportedExtensions = ["*.py" ]; //["*.py", "*.json"];
    private static readonly JsonSerializerOptions Options = new() { WriteIndented = true };

    /// <summary>
    /// Compares two folders and builds a tree of comparison items for supported files (Python and JSON).
    /// </summary>
    public static ObservableCollection<ComparisonItem> CompareDirectories(string leftPath, string rightPath)
    {
        var result = new ObservableCollection<ComparisonItem>();

        if (!Directory.Exists(leftPath) && !Directory.Exists(rightPath))
        {
            return result;
        }

        BuildComparisonTree(leftPath, rightPath, string.Empty, result);
        return result;
    }

    private static void BuildComparisonTree(string leftBasePath, string rightBasePath, string relativePath, 
        ObservableCollection<ComparisonItem> items)
    {
        string leftDir = string.IsNullOrEmpty(relativePath) ? leftBasePath : Path.Combine(leftBasePath, relativePath);
        string rightDir = string.IsNullOrEmpty(relativePath) ? rightBasePath : Path.Combine(rightBasePath, relativePath);

        bool leftExists = Directory.Exists(leftDir);
        bool rightExists = Directory.Exists(rightDir);

        // Get all supported files from both sides (Python and JSON)
        var leftFiles = leftExists 
            ? GetSupportedFiles(leftDir).ToHashSet(StringComparer.OrdinalIgnoreCase)
            : [];
        var rightFiles = rightExists 
            ? GetSupportedFiles(rightDir).ToHashSet(StringComparer.OrdinalIgnoreCase)
            : [];

        // Get all subdirectories from both sides
        var leftDirs = leftExists
            ? Directory.GetDirectories(leftDir).Select(Path.GetFileName).ToHashSet(StringComparer.OrdinalIgnoreCase)
            : [];
        var rightDirs = rightExists
            ? Directory.GetDirectories(rightDir).Select(Path.GetFileName).ToHashSet(StringComparer.OrdinalIgnoreCase)
            : [];

        // Combine all unique names
        var allFiles = leftFiles.Union(rightFiles, StringComparer.OrdinalIgnoreCase).OrderBy(f => f, StringComparer.OrdinalIgnoreCase);
        var allDirs = leftDirs.Union(rightDirs, StringComparer.OrdinalIgnoreCase)
            .Where(d => !d!.Equals("lib", StringComparison.OrdinalIgnoreCase)) // Exclude lib folder
            .OrderBy(d => d, StringComparer.OrdinalIgnoreCase);

        // Process subdirectories first
        foreach (var dirName in allDirs)
        {
            string dirRelativePath = string.IsNullOrEmpty(relativePath) ? dirName! : Path.Combine(relativePath, dirName!);
            string leftDirPath = Path.Combine(leftBasePath, dirRelativePath);
            string rightDirPath = Path.Combine(rightBasePath, dirRelativePath);

            var folderItem = new ComparisonItem
            {
                Name = dirName!,
                RelativePath = dirRelativePath,
                LeftFullPath = Directory.Exists(leftDirPath) ? leftDirPath : null,
                RightFullPath = Directory.Exists(rightDirPath) ? rightDirPath : null,
                IsFolder = true,
            };

            // Recursively build children
            BuildComparisonTree(leftBasePath, rightBasePath, dirRelativePath, folderItem.Children);

            // Only add folder if it contains supported files (directly or in subfolders)
            if (folderItem.Children.Count > 0)
            {
                // Set folder status based on children
                if (folderItem.Children.Any(c => c.Status != FileComparisonStatus.Same))
                {
                    folderItem.Status = FileComparisonStatus.ContainsDifferences;
                }

                items.Add(folderItem);
            }
        }

        // Process files in parallel for better performance
        var fileList = allFiles.ToList();
        var fileItems = new ConcurrentBag<ComparisonItem>();

        Parallel.ForEach(fileList, fileName =>
        {
            string fileRelativePath = string.IsNullOrEmpty(relativePath) ? fileName! : Path.Combine(relativePath, fileName!);
            string? leftFilePath = leftFiles.Contains(fileName!) ? Path.Combine(leftDir, fileName!) : null;
            string? rightFilePath = rightFiles.Contains(fileName!) ? Path.Combine(rightDir, fileName!) : null;

            var fileItem = new ComparisonItem
            {
                Name = fileName!,
                RelativePath = fileRelativePath,
                LeftFullPath = leftFilePath,
                RightFullPath = rightFilePath,
                IsFolder = false,
                IsPythonScript = Path.GetExtension(fileName!).Contains("py", StringComparison.OrdinalIgnoreCase),
            };

            // Determine status
            if (leftFilePath is null)
            {
                fileItem.Status = FileComparisonStatus.RightOnly;
            }
            else if (rightFilePath is null)
            {
                fileItem.Status = FileComparisonStatus.LeftOnly;
            }
            else
            {
                // Both exist - compare content
                fileItem.Status = AreFilesIdentical(leftFilePath, rightFilePath) 
                    ? FileComparisonStatus.Same 
                    : FileComparisonStatus.Different;
            }

            // Check for lock status
            if (leftFilePath is not null)
            {
                fileItem.IsLocked = IsFileLocked(leftFilePath);
            }

            if (rightFilePath is not null)
            {
                fileItem.IsLockedRight = IsFileLocked(rightFilePath);
            }

            fileItems.Add(fileItem);
        });

        // Add sorted results to maintain consistent ordering
        foreach (var fileItem in fileItems.OrderBy(f => f.Name, StringComparer.OrdinalIgnoreCase))
        {
            items.Add(fileItem);
        }
    }

    /// <summary>
    /// Checks if a file's first line contains a lock directive.
    /// Uses buffered reading to only read first line without loading entire file.
    /// </summary>
    public static bool IsFileLocked(string filePath)
    {
        try
        {
            // Read only first 256 bytes - sufficient for lock pattern check
            byte[] buffer = ArrayPool<byte>.Shared.Rent(256);
            try
            {
                using var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.Read, 256, FileOptions.SequentialScan);
                int bytesRead = fs.Read(buffer, 0, 256);
                if (bytesRead == 0)
                {
                    return false;
                }

                // Find newline or use all bytes read
                int lineEnd = Array.IndexOf(buffer, (byte)'\n', 0, bytesRead);
                int length = lineEnd >= 0 ? lineEnd : bytesRead;

                ReadOnlySpan<char> firstLine = System.Text.Encoding.UTF8.GetString(buffer.AsSpan(0, length));
                return firstLine.Contains(LockPattern, StringComparison.OrdinalIgnoreCase);
            }
            finally
            {
                ArrayPool<byte>.Shared.Return(buffer);
            }
        }
        catch
        {
            return false;
        }
    }

    private const int CompareBufferSize = 81920; // 80KB buffer for file comparison

    /// <summary>
    /// Quickly checks if two files have identical content using buffered byte comparison.
    /// </summary>
    private static bool AreFilesIdentical(string path1, string path2)
    {
        try
        {
            var info1 = new FileInfo(path1);
            var info2 = new FileInfo(path2);

            // Quick check: different sizes means different content
            if (info1.Length != info2.Length)
            {
                return false;
            }

            // Empty files are identical
            if (info1.Length == 0)
            {
                return true;
            }

            // Use buffered byte comparison - much faster than string comparison
            byte[] buffer1 = ArrayPool<byte>.Shared.Rent(CompareBufferSize);
            byte[] buffer2 = ArrayPool<byte>.Shared.Rent(CompareBufferSize);
            try
            {
                using var fs1 = new FileStream(path1, FileMode.Open, FileAccess.Read, FileShare.Read, CompareBufferSize, FileOptions.SequentialScan);
                using var fs2 = new FileStream(path2, FileMode.Open, FileAccess.Read, FileShare.Read, CompareBufferSize, FileOptions.SequentialScan);

                int bytesRead1, bytesRead2;
                while ((bytesRead1 = fs1.Read(buffer1, 0, CompareBufferSize)) > 0)
                {
                    bytesRead2 = fs2.Read(buffer2, 0, CompareBufferSize);
                    if (bytesRead1 != bytesRead2)
                    {
                        return false;
                    }

                    if (!buffer1.AsSpan(0, bytesRead1).SequenceEqual(buffer2.AsSpan(0, bytesRead2)))
                    {
                        return false;
                    }
                }

                return true;
            }
            finally
            {
                ArrayPool<byte>.Shared.Return(buffer1);
                ArrayPool<byte>.Shared.Return(buffer2);
            }
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Compares two files and generates a detailed diff result.
    /// JSON files are automatically prettified for readable comparison.
    /// </summary>
    public static FileComparisonResult CompareFiles(string? leftPath, string? rightPath, string relativePath)
    {
        var result = new FileComparisonResult
        {
            LeftPath = leftPath ?? string.Empty,
            RightPath = rightPath ?? string.Empty,
            RelativePath = relativePath
        };

        string[] leftLines = [];
        string[] rightLines = [];
        bool leftExists = leftPath is not null && File.Exists(leftPath);
        bool rightExists = rightPath is not null && File.Exists(rightPath);

        if (leftExists)
        {
            leftLines = ReadFileLines(leftPath!);
        }

        if (rightExists)
        {
            rightLines = ReadFileLines(rightPath!);
        }

        // Determine status
        FileComparisonStatus status;
        if (!leftExists && !rightExists)
        {
            status = FileComparisonStatus.Same;
        }
        else if (!leftExists)
        {
            status = FileComparisonStatus.RightOnly;
        }
        else if (!rightExists)
        {
            status = FileComparisonStatus.LeftOnly;
        }
        else
        {
            status = leftLines.SequenceEqual(rightLines) ? FileComparisonStatus.Same : FileComparisonStatus.Different;
        }

        // Generate diff using LCS algorithm
        var diffLines = GenerateDiff(leftLines, rightLines);

        int added = 0, removed = 0, unchanged = 0;
        foreach (var line in diffLines)
        {
            result.DiffLines.Add(line);
            switch (line.Type)
            {
                case DiffLineType.Added: added++; break;
                case DiffLineType.Removed: removed++; break;
                case DiffLineType.Unchanged: unchanged++; break;
            }
        }

        return new FileComparisonResult
        {
            LeftPath = leftPath ?? string.Empty,
            RightPath = rightPath ?? string.Empty,
            RelativePath = relativePath,
            Status = status,
            IsLeftLocked = leftExists && IsFileLocked(leftPath!),
            IsRightLocked = rightExists && IsFileLocked(rightPath!),
            DiffLines = result.DiffLines,
            AddedLines = added,
            RemovedLines = removed,
            UnchangedLines = unchanged
        };
    }

    /// <summary>
    /// Generates a unified diff using the LCS (Longest Common Subsequence) algorithm.
    /// Uses pre-computed hash codes for O(1) line comparison.
    /// </summary>
    private static ObservableCollection<DiffLine> GenerateDiff(string[] leftLines, string[] rightLines)
    {
        // Pre-compute hash codes for fast comparison
        int[] leftHashes = new int[leftLines.Length];
        int[] rightHashes = new int[rightLines.Length];

        for (int k = 0; k < leftLines.Length; k++)
        {
            leftHashes[k] = leftLines[k].GetHashCode();
        }

        for (int k = 0; k < rightLines.Length; k++)
        {
            rightHashes[k] = rightLines[k].GetHashCode();
        }

        // Build LCS table using hash comparison
        int[,] lcs = BuildLcsTableWithHashes(leftLines, rightLines, leftHashes, rightHashes);

        // Backtrack to generate diff - pre-allocate capacity
        int i = leftLines.Length;
        int j = rightLines.Length;
        var tempResult = new List<DiffLine>(leftLines.Length + rightLines.Length);

        while (i > 0 || j > 0)
        {
            if (i > 0 && j > 0 && leftHashes[i - 1] == rightHashes[j - 1] && leftLines[i - 1] == rightLines[j - 1])
            {
                // Lines are the same (hash match + string equality for collision safety)
                tempResult.Add(new DiffLine
                {
                    Type = DiffLineType.Unchanged,
                    Content = leftLines[i - 1],
                    LeftLineNumber = i,
                    RightLineNumber = j
                });
                i--;
                j--;
            }
            else if (j > 0 && (i == 0 || lcs[i, j - 1] >= lcs[i - 1, j]))
            {
                // Line was added on right
                tempResult.Add(new DiffLine
                {
                    Type = DiffLineType.Added,
                    Content = rightLines[j - 1],
                    LeftLineNumber = null,
                    RightLineNumber = j
                });
                j--;
            }
            else if (i > 0)
            {
                // Line was removed from left
                tempResult.Add(new DiffLine
                {
                    Type = DiffLineType.Removed,
                    Content = leftLines[i - 1],
                    LeftLineNumber = i,
                    RightLineNumber = null
                });
                i--;
            }
        }

        // Reverse and create ObservableCollection in one shot
        tempResult.Reverse();
        return new ObservableCollection<DiffLine>(tempResult);
    }

    /// <summary>
    /// Builds the LCS (Longest Common Subsequence) table using pre-computed hash codes.
    /// Hash comparison is O(1) vs O(n) for string comparison.
    /// </summary>
    private static int[,] BuildLcsTableWithHashes(string[] left, string[] right, int[] leftHashes, int[] rightHashes)
    {
        int m = left.Length;
        int n = right.Length;
        int[,] table = new int[m + 1, n + 1];

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                // Fast hash comparison first, then string equality only on hash match
                if (leftHashes[i - 1] == rightHashes[j - 1] && left[i - 1] == right[j - 1])
                {
                    table[i, j] = table[i - 1, j - 1] + 1;
                }
                else
                {
                    table[i, j] = Math.Max(table[i - 1, j], table[i, j - 1]);
                }
            }
        }

        return table;
    }

    /// <summary>
    /// Updates the status of parent folders based on their children's status.
    /// </summary>
    public static void UpdateFolderStatuses(ObservableCollection<ComparisonItem> items)
    {
        foreach (var item in items)
        {
            if (item.IsFolder)
            {
                UpdateFolderStatuses(item.Children);

                if (item.Children.Any(c => c.Status != FileComparisonStatus.Same))
                {
                    item.Status = FileComparisonStatus.ContainsDifferences;
                }
                else
                {
                    item.Status = FileComparisonStatus.Same;
                }
            }
        }
    }

    /// <summary>
    /// Gets all file names with supported extensions from a directory.
    /// </summary>
    private static IEnumerable<string?> GetSupportedFiles(string directory)
    {
        return SupportedExtensions
            .SelectMany(ext => Directory.GetFiles(directory, ext))
            .Select(Path.GetFileName);
    }

    /// <summary>
    /// Checks if a file is a JSON file based on extension.
    /// </summary>
    private static bool IsJsonFile(string? filePath)
    {
        if (string.IsNullOrEmpty(filePath))
        {
            return false;
        }

        return Path.GetExtension(filePath).Equals(".json", StringComparison.OrdinalIgnoreCase);
    }

    /// <summary>
    /// Prettifies minified JSON content for readable diff comparison.
    /// </summary>
    private static string PrettifyJson(string content)
    {
        try
        {
            using var doc = JsonDocument.Parse(content);
            return JsonSerializer.Serialize(doc.RootElement, Options);
        }
        catch
        {
            // If JSON parsing fails, return original content
            return content;
        }
    }

    /// <summary>
    /// Reads file content, prettifying JSON files for better diff comparison.
    /// </summary>
    private static string[] ReadFileLines(string filePath)
    {
        if (IsJsonFile(filePath))
        {
            string content = File.ReadAllText(filePath);
            string[] splitContent = content.Split(Environment.NewLine);
            string prettified = PrettifyJson(splitContent[1]);         
            return [.. prettified.Split(Environment.NewLine, StringSplitOptions.None).Where(line => !string.IsNullOrEmpty(line) || line == string.Empty)];
        }

        return File.ReadAllLines(filePath);
    }
}
