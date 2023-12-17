import datetime


class TimeUtils:

    @staticmethod
    def get_utc_now():
        """Return the current time in UTC."""
        return datetime.datetime.utcnow()

    @staticmethod
    def get_time_delta(minutes):
        """Return a time delta object for the specified number of minutes."""
        return datetime.timedelta(minutes=minutes)

    @staticmethod
    def format_rfc3339(dt):
        """Convert a datetime object into RFC3339 format."""
        return dt.isoformat() + "Z"

    @staticmethod
    def get_past_time(minutes):
        """Return the time 'minutes' minutes ago, in RFC3339 format."""
        now = TimeUtils.get_utc_now()
        past_time = now - TimeUtils.get_time_delta(minutes)
        return TimeUtils.format_rfc3339(past_time)
