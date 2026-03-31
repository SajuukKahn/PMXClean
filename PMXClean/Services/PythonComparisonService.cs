namespace PMXClean.Services;

using System.Collections.ObjectModel;
using System.IO;
using PMXClean.Models;

/// <summary>
/// Service for comparing Python files and folders using LCS-based diff algorithm.
/// </summary>
public static class PythonComparisonService
{
    private const string LockPattern = "#lock";

    /// <summary>
    /// Compares two folders and builds a tree of comparison items for Python files.
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

        // Get all Python files from both sides
        var leftFiles = leftExists 
            ? Directory.GetFiles(leftDir, "*.py").Select(Path.GetFileName).ToHashSet(StringComparer.OrdinalIgnoreCase)
            : [];
        var rightFiles = rightExists 
            ? Directory.GetFiles(rightDir, "*.py").Select(Path.GetFileName).ToHashSet(StringComparer.OrdinalIgnoreCase)
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
                IsFolder = true
            };

            // Recursively build children
            BuildComparisonTree(leftBasePath, rightBasePath, dirRelativePath, folderItem.Children);

            // Only add folder if it contains Python files (directly or in subfolders)
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

        // Process files
        foreach (var fileName in allFiles)
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
                IsFolder = false
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

            items.Add(fileItem);
        }
    }

    /// <summary>
    /// Checks if a file's first line contains a lock directive.
    /// </summary>
    public static bool IsFileLocked(string filePath)
    {
        try
        {
            using var reader = new StreamReader(filePath);
            string? firstLine = reader.ReadLine();
            if (firstLine is null)
            {
                return false;
            }

            return firstLine.Contains(LockPattern, StringComparison.OrdinalIgnoreCase);
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Quickly checks if two files have identical content.
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

            // Compare content
            string content1 = File.ReadAllText(path1);
            string content2 = File.ReadAllText(path2);

            return content1 == content2;
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Compares two files and generates a detailed diff result.
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
            leftLines = File.ReadAllLines(leftPath!);
        }

        if (rightExists)
        {
            rightLines = File.ReadAllLines(rightPath!);
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
    /// </summary>
    private static ObservableCollection<DiffLine> GenerateDiff(string[] leftLines, string[] rightLines)
    {
        var result = new ObservableCollection<DiffLine>();

        // Build LCS table
        int[,] lcs = BuildLcsTable(leftLines, rightLines);

        // Backtrack to generate diff
        int i = leftLines.Length;
        int j = rightLines.Length;
        var tempResult = new List<DiffLine>();

        while (i > 0 || j > 0)
        {
            if (i > 0 && j > 0 && leftLines[i - 1] == rightLines[j - 1])
            {
                // Lines are the same
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

        // Reverse to get correct order
        tempResult.Reverse();

        foreach (var line in tempResult)
        {
            result.Add(line);
        }

        return result;
    }

    /// <summary>
    /// Builds the LCS (Longest Common Subsequence) table for diff calculation.
    /// </summary>
    private static int[,] BuildLcsTable(string[] left, string[] right)
    {
        int m = left.Length;
        int n = right.Length;
        int[,] table = new int[m + 1, n + 1];

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (left[i - 1] == right[j - 1])
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
}
