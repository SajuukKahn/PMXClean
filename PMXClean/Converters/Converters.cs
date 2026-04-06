namespace PMXClean.Converters
{
    using System.Globalization;
    using System.Windows;
    using System.Windows.Data;
    using System.Windows.Media;
    using PMXClean.Models;

    /// <summary>
    /// Converts a non-null value to true, null to false.
    /// </summary>
    public class NotNullToBoolConverter : IValueConverter
    {
        public static NotNullToBoolConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            return value is not null;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    public class BooleanInversionConverter: IValueConverter
    {
        public static BooleanInversionConverter Instance { get; } = new();
        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            return value is bool boolValue ? !boolValue : false;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts a non-null value to Visible, null to Collapsed.
    /// </summary>
    public class NotNullToVisibilityConverter : IValueConverter
    {
        public static NotNullToVisibilityConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            return value is not null ? Visibility.Visible : Visibility.Collapsed;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts a null value to Visible, non-null to Collapsed.
    /// </summary>
    public class NullToVisibilityConverter : IValueConverter
    {
        public static NullToVisibilityConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            return value is null ? Visibility.Visible : Visibility.Collapsed;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts a non-zero value to Visible, zero to Collapsed.
    /// </summary>
    public class NotZeroToVisibilityConverter : IValueConverter
    {
        public static NotZeroToVisibilityConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is int intValue)
            {
                if (parameter is not null && parameter is string s && bool.TryParse(s, out bool invert) && invert)
                {
                    return intValue > 0 ? Visibility.Collapsed : Visibility.Visible;
                }

                return intValue > 0 ? Visibility.Visible : Visibility.Collapsed;
            }

            return Visibility.Collapsed;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts false to Visible, true to Collapsed.
    /// </summary>
    public class InverseBooleanToVisibilityConverter : IValueConverter
    {
        public static InverseBooleanToVisibilityConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is bool boolValue)
            {
                return boolValue ? Visibility.Collapsed : Visibility.Visible;
            }

            return Visibility.Visible;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts SystemStatus to a color brush.
    /// </summary>
    public class SystemStatusToBrushConverter : IValueConverter
    {
        public static SystemStatusToBrushConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is SystemStatus status)
            {
                return status switch
                {
                    SystemStatus.Good => new SolidColorBrush(Color.FromRgb(76, 175, 80)),      // Green
                    SystemStatus.Warning => new SolidColorBrush(Color.FromRgb(255, 152, 0)),   // Orange
                    SystemStatus.Error => new SolidColorBrush(Color.FromRgb(244, 67, 54)),     // Red
                    SystemStatus.Info => new SolidColorBrush(Color.FromRgb(33, 150, 243)),     // Blue
                    SystemStatus.Unknown => new SolidColorBrush(Color.FromRgb(158, 158, 158)), // Gray
                    _ => new SolidColorBrush(Color.FromRgb(158, 158, 158))
                };
            }

            return new SolidColorBrush(Color.FromRgb(158, 158, 158));
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts SystemStatus to a Material Design icon kind.
    /// </summary>
    public class SystemStatusToIconConverter : IValueConverter
    {
        public static SystemStatusToIconConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is SystemStatus status)
            {
                return status switch
                {
                    SystemStatus.Good => "CheckCircle",
                    SystemStatus.Warning => "AlertCircle",
                    SystemStatus.Error => "CloseCircle",
                    SystemStatus.Info => "InformationOutline",
                    SystemStatus.Unknown => "HelpCircle",
                    _ => "HelpCircle"
                };
            }

            return "HelpCircle";
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts EventLogLevel to a color brush.
    /// </summary>
    public class EventLogLevelToBrushConverter : IValueConverter
    {
        public static EventLogLevelToBrushConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is EventLogLevel level)
            {
                return level switch
                {
                    EventLogLevel.Critical => new SolidColorBrush(Color.FromRgb(183, 28, 28)),    // Dark Red
                    EventLogLevel.Error => new SolidColorBrush(Color.FromRgb(244, 67, 54)),       // Red
                    EventLogLevel.Warning => new SolidColorBrush(Color.FromRgb(255, 152, 0)),     // Orange
                    EventLogLevel.Information => new SolidColorBrush(Color.FromRgb(33, 150, 243)), // Blue
                    EventLogLevel.Verbose => new SolidColorBrush(Color.FromRgb(158, 158, 158)),   // Gray
                    _ => new SolidColorBrush(Color.FromRgb(158, 158, 158))
                };
            }

            return new SolidColorBrush(Color.FromRgb(158, 158, 158));
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts EventLogLevel to a Material Design icon kind.
    /// </summary>
    public class EventLogLevelToIconConverter : IValueConverter
    {
        public static EventLogLevelToIconConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is EventLogLevel level)
            {
                return level switch
                {
                    EventLogLevel.Critical => "AlertOctagon",
                    EventLogLevel.Error => "CloseCircle",
                    EventLogLevel.Warning => "AlertCircle",
                    EventLogLevel.Information => "InformationOutline",
                    EventLogLevel.Verbose => "MessageTextOutline",
                    _ => "HelpCircle"
                };
            }

            return "HelpCircle";
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts text to TextWrapping: NoWrap if text contains newlines, Wrap otherwise.
    /// Useful for preserving formatting of stack traces while wrapping single-line text.
    /// </summary>
    public class NewlineToTextWrappingConverter : IValueConverter
    {
        public static NewlineToTextWrappingConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is string text)
            {
                bool hasNewlines = text.Contains('\n') || text.Contains('\r');
                return hasNewlines ? TextWrapping.NoWrap : TextWrapping.Wrap;
            }

            return TextWrapping.Wrap;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts a list of strings to a newline-separated string for tooltip display.
    /// </summary>
    public class ListToStringConverter : IValueConverter
    {
        public static ListToStringConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is IEnumerable<string> list)
            {
                var items = list.ToList();
                if (items.Count == 0)
                {
                    return "No items";
                }

                return string.Join(Environment.NewLine, items);
            }

            return string.Empty;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Converts a non-null value to true, null to false.
    /// </summary>
    public class NotNullToBooleanConverter : IValueConverter
    {
        public static NotNullToBooleanConverter Instance { get; } = new();

        public object Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            return value is not null;
        }

        public object ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Multi-value converter that returns Visible if all boolean inputs are true, Collapsed otherwise.
    /// </summary>
    public class AllTrueToVisibilityMultiConverter : IMultiValueConverter
    {
        public static AllTrueToVisibilityMultiConverter Instance { get; } = new();

        public object Convert(object[] values, Type targetType, object parameter, CultureInfo culture)
        {
            foreach (var value in values)
            {
                if (value is not bool boolValue || !boolValue)
                {
                    return Visibility.Collapsed;
                }
            }

            return Visibility.Visible;
        }

        public object[] ConvertBack(object value, Type[] targetTypes, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
