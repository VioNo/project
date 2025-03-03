from datetime import datetime
import pytz

# Example datetime with time zone information
datetime_with_tz = datetime.now(pytz.UTC)

# Extract only the date
date_only = datetime_with_tz.date()

print(date_only)