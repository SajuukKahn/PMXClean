namespace PMXClean.Behaviors;

using System.Windows;
using System.Windows.Controls;

/// <summary>
/// Attached behavior that focuses a TextBox and selects all text when a trigger property becomes true.
/// </summary>
public static class FocusSelectAllBehavior
{
    public static readonly DependencyProperty IsFocusedProperty = DependencyProperty.RegisterAttached("IsFocused", typeof(bool), typeof(FocusSelectAllBehavior), new PropertyMetadata(false, OnIsFocusedChanged));

    public static bool GetIsFocused(DependencyObject obj) => (bool)obj.GetValue(IsFocusedProperty);

    public static void SetIsFocused(DependencyObject obj, bool value) => obj.SetValue(IsFocusedProperty, value);

    private static void OnIsFocusedChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
    {
        if (d is TextBox textBox && e.NewValue is true)
        {
            textBox.Dispatcher.BeginInvoke(() =>
            {
                textBox.Focus();
                textBox.SelectAll();
            }, System.Windows.Threading.DispatcherPriority.Input);
        }
    }
}
