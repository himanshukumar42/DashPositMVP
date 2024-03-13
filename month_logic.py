import pandas as pd

def month_to_weekly(year, month):
    # Get the start and end dates of the month
    start_date = pd.Timestamp(year, month, 1)
    end_date = pd.Timestamp(year, month, pd.Timestamp(year, month+1, 1).day)

    # Generate weekly intervals
    weekly_intervals = pd.date_range(start=start_date, end=end_date, freq='W-SUN')

    return weekly_intervals

# Example usage
year = 2024
month = 3
weekly_intervals = month_to_weekly(year, month)
print("Weekly intervals for {}/{}:".format(month, year))
for idx, interval in enumerate(weekly_intervals):
    print("Week {}: {} to {}".format(idx + 1, interval.strftime('%Y-%m-%d'), (interval + pd.DateOffset(days=6)).strftime('%Y-%m-%d')))
