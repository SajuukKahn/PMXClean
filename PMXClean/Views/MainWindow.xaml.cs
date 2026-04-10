namespace PMXClean.Views;

using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using PMXClean.Models;
using PMXClean.ViewModels;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    /// <summary>
    /// Handles the click event for page selection from the ListBox.
    /// </summary>
    private void PageListBoxItem_Click(object sender, System.Windows.Input.MouseButtonEventArgs e)
    {
        // Get the clicked ListBoxItem
        var listBoxItem = sender as ListBoxItem;
        if (listBoxItem?.Content is PageInfo page)
        {
            // Get the ViewModel and call the SelectPage command
            if (DataContext is MainViewModel viewModel)
            {
                viewModel.SelectPageCommand.Execute(page);
            }

            // Close the popup by unchecking the toggle button
            if (FindName("PageSelectionButton") is ToggleButton toggleButton)
            {
                toggleButton.IsChecked = false;
            }
        }
    }

    /// <summary>
    /// Handles the selection changed event for the locked files TreeView.
    /// </summary>
    private void LockedFilesTreeView_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
    {
        if (DataContext is MainViewModel viewModel && e.NewValue is LockedFileItem lockedFileItem)
        {
            viewModel.SelectedLockedFile = lockedFileItem;
        }
    }

    /// <summary>
    /// Handles drag-and-drop of .machine backup files onto the header.
    /// </summary>
    private async void ColorZone_Drop(object sender, DragEventArgs e)
    {
        if (e.Data.GetDataPresent(DataFormats.FileDrop))
        {
            var files = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (files is not null && DataContext is MainViewModel viewModel)
            {
                await viewModel.HandleFileDropAsync(files);
            }
        }
    }

    /// <summary>
    /// Handles drag-and-drop of .machine backup files onto the left backup drop zone.
    /// </summary>
    private async void LeftBackupDrop_Drop(object sender, DragEventArgs e)
    {
        if (e.Data.GetDataPresent(DataFormats.FileDrop))
        {
            var files = (string[])e.Data.GetData(DataFormats.FileDrop);
            var machineFile = files?.FirstOrDefault(f => f.EndsWith(".machine", StringComparison.OrdinalIgnoreCase));

            if (machineFile is not null && DataContext is MainViewModel viewModel)
            {
                await viewModel.ComparisonViewModel.LoadLeftBackupFromPathAsync(machineFile);
            }
        }
    }

    /// <summary>
    /// Handles drag-and-drop of .machine backup files onto the right backup drop zone.
    /// </summary>
    private async void RightBackupDrop_Drop(object sender, DragEventArgs e)
    {
        if (e.Data.GetDataPresent(DataFormats.FileDrop))
        {
            var files = (string[])e.Data.GetData(DataFormats.FileDrop);
            var machineFile = files?.FirstOrDefault(f => f.EndsWith(".machine", StringComparison.OrdinalIgnoreCase));

            if (machineFile is not null && DataContext is MainViewModel viewModel)
            {
                await viewModel.ComparisonViewModel.LoadRightBackupFromPathAsync(machineFile);
            }
        }
    }
}
