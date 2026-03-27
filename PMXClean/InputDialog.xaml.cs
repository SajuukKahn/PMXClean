namespace PMXClean
{
    using System.Windows;

    /// <summary>
    /// Input dialog for getting text input from the user
    /// </summary>
    public partial class InputDialog : Window
    {
        public string ResponseText => ResponseTextBox.Text;

        public InputDialog(string title, string prompt, string defaultValue = "")
        {
            InitializeComponent();
            
            Title = title;
            PromptTextBlock.Text = prompt;
            ResponseTextBox.Text = defaultValue;
            
            ResponseTextBox.Focus();
            ResponseTextBox.SelectAll();
        }

        private void OK_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}
