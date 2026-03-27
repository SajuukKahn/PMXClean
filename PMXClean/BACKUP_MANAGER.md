# Enhanced Backup Manager - Feature Documentation

## Overview
The backup system has been completely redesigned to support **multiple named backup instances** with full management capabilities. Users can now maintain multiple backup snapshots with descriptive names, making it easy to organize and restore different versions.

## New Features

### 1. **Multiple Backup Instances**
- Create unlimited named backups
- Each backup is stored in `Backups\[BackupName]\` folder
- Backups are independent and can be managed separately
- Default naming: `Backup_YYYYMMDD_HHmmss` (auto-generated timestamp)

### 2. **Backup Selection ComboBox**
- Dropdown list shows all available backups
- Sorted by last modified date (newest first)
- Select any backup to view details or perform operations
- Current selection is highlighted

### 3. **Backup Management Buttons**

#### **New... Button**
- Creates a new backup instance
- Opens input dialog for custom name
- Auto-suggests timestamped name
- Validates and sanitizes backup names
- Prevents duplicate names

#### **Rename... Button**
- Renames selected backup instance
- Opens input dialog with current name
- Updates all references automatically
- Prevents conflicts with existing names

#### **Delete Button**
- Permanently deletes selected backup
- Shows confirmation dialog with backup name
- Cannot be undone
- Automatically selects next available backup

### 4. **Backup Information Display**
Shows real-time information about selected backup:
- **Created**: Initial creation date and time
- **Modified**: Last modification date and time
- **Files**: Total number of files
- **Size**: Total size in megabytes

### 5. **Enhanced Backup Operations**

#### **Copy All Files** (New!)
- Backs up entire target directory
- Includes all file types
- Preserves directory structure
- One-click complete backup

#### **Selective Backups**
All existing backup operations now work with the selected backup:
- Copy JSON
- Copy Retention
- Copy Python
- Copy DLLs
- Copy Page Stubs

#### **Restore to Target**
- Restores selected backup to target path
- Shows backup name in confirmation
- Overwrites existing files
- Preserves file timestamps

## User Interface Layout

```
┌─────────────────────────────────────────────┐
│         Backup Manager                      │
├─────────────────────────────────────────────┤
│  Select Backup Instance:                    │
│  ┌─────────────────────────────────────┐   │
│  │ Backup_20240115_143022         ▼    │   │
│  └─────────────────────────────────────┘   │
│                                              │
│  [New...]  [Rename...]  [Delete]            │
│                                              │
│  Created: 1/15/2024 2:30 PM                 │
│  Modified: 1/15/2024 3:45 PM                │
│  Files: 1,234 (156.78 MB)                   │
├─────────────────────────────────────────────┤
│  Backup Operations                          │
├─────────────────────────────────────────────┤
│  [Copy All Files]                           │
│  [Copy JSON]                                │
│  [Copy Retention]                           │
│  [Copy Python]                              │
│  [Copy DLLs]                                │
│  [Copy Page Stubs]                          │
│  ─────────────────                          │
│  [Restore to Target]                        │
└─────────────────────────────────────────────┘
```

## Usage Workflows

### Creating a New Backup

1. Click **"New..."** button
2. Enter descriptive name (e.g., "Pre-Update-Backup")
3. Click **OK**
4. New backup is created and selected
5. Use backup operation buttons to populate it

### Quick Backup with All Files

1. Select or create a backup
2. Click **"Copy All Files"**
3. All files are copied to selected backup
4. Backup info updates automatically

### Selective Backup

1. Select or create a backup
2. Click specific file type button (e.g., "Copy Python")
3. Only those files are backed up
4. Repeat for other file types as needed

### Restoring from Backup

1. Select the backup you want to restore
2. Review backup info to confirm it's the right one
3. Click **"Restore to Target"**
4. Confirm the operation
5. Files are restored to target path

### Managing Old Backups

1. Select an old backup from dropdown
2. Review its info to determine if needed
3. Click **"Delete"** if no longer needed
4. Confirm deletion
5. Backup is permanently removed

### Renaming Backups

1. Select the backup to rename
2. Click **"Rename..."**
3. Enter new descriptive name
4. Click **OK**
5. Backup is renamed, selection maintained

## Technical Details

### Backup Storage Structure
```
Backups/
├── Backup_20240115_143022/
│   ├── *.py
│   ├── *.json
│   └── [directory structure preserved]
├── Pre-Release-Backup/
│   └── [files]
└── Test-Configuration/
    └── [files]
```

### Key Implementation Features

#### **Backup Path Management**
```csharp
private readonly string backupsRootDirectory;  // "Backups" folder
private string? currentBackupPath;             // Selected backup path
```

#### **Auto-Loading Backups**
- Scans `Backups\` folder on startup
- Populates ComboBox with available backups
- Sorts by last modified date (newest first)
- Selects most recent backup by default

#### **Name Sanitization**
- Removes invalid filename characters
- Replaces with underscores
- Ensures filesystem compatibility
- Prevents path traversal

#### **Real-Time Info Updates**
- Recalculates on every selection change
- Counts files recursively
- Sums file sizes accurately
- Shows formatted dates

### Error Handling

All operations include comprehensive error handling:
- **No backup selected**: Friendly prompt to create/select
- **Duplicate names**: Warning with existing name
- **Missing backup**: Error message with details
- **IO errors**: Full exception messages displayed

## Migration from Old System

### Automatic Migration
If you have an existing `backup\` folder from the old system:
1. Rename it to a descriptive name (e.g., "Legacy-Backup")
2. Move it into the `Backups\` folder
3. It will appear in the ComboBox automatically

### Manual Migration
```
Old: backup\
New: Backups\Legacy-Backup\
```

## Benefits Over Previous System

| Feature | Old System | New System |
|---------|-----------|------------|
| Backup Count | 1 (overwrites) | Unlimited |
| Naming | Fixed "backup" | Custom names |
| Selection | N/A (always "backup") | ComboBox dropdown |
| Information | None | Date, size, count |
| Management | Manual filesystem | Built-in UI |
| Deletion | Manual | Confirmation dialog |
| Rename | Manual | Input dialog |
| Restore Info | None | Shows backup name |

## Best Practices

### Naming Conventions
- **Use dates**: `Backup_2024-01-15`
- **Use descriptions**: `Pre-Version-2.0-Update`
- **Use context**: `Before-Config-Change`
- **Avoid special chars**: Use hyphens and underscores

### Backup Strategy
1. **Before major changes**: Create named backup
2. **Regular backups**: Use timestamped names
3. **Selective backups**: Only back up what changed
4. **Full backups**: Use "Copy All Files" periodically
5. **Cleanup old backups**: Delete when no longer needed

### Organization Tips
- Keep 3-5 recent backups
- Name backups by purpose, not just date
- Delete backups after verifying new ones
- Use descriptive names for important milestones

## Keyboard Shortcuts

While the ComboBox is focused:
- **↑/↓**: Navigate backups
- **Enter**: Confirm selection
- **Esc**: Cancel selection

## Future Enhancements (Potential)

- 📊 Backup size quotas
- 🔍 Search/filter backups
- 📅 Automatic backup scheduling
- 🗜️ Compression for storage
- 📝 Backup notes/descriptions
- 📈 Backup history graph
- ⚡ Incremental backups
- 🔄 Backup comparison tool

## Troubleshooting

### ComboBox is Empty
- No backups exist yet
- Click "New..." to create first backup
- Or copy files from old `backup\` folder

### Cannot Delete Backup
- Files may be in use
- Close other applications
- Check file permissions
- Try again after restart

### Backup Info Shows Error
- Backup folder may be corrupt
- Try accessing folder manually
- Delete and recreate if needed

### "Backup not found" Error
- Backup was deleted outside app
- ComboBox needs refresh
- Restart application

## Summary

The enhanced backup manager provides a professional-grade backup solution with:
- ✅ Multiple named instances
- ✅ Easy creation and management
- ✅ Visual feedback and information
- ✅ Safe deletion with confirmations
- ✅ Flexible rename capability
- ✅ Quick restore operations
- ✅ Organized folder structure

This upgrade transforms backup management from a single-folder system into a powerful, user-friendly backup solution suitable for production environments.
