namespace PMXClean.Converters
{
    using System.Globalization;
    using System.Windows;
    using System.Windows.Data;

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
}
