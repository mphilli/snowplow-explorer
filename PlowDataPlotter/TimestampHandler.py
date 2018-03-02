from datetime import datetime as dt


class Timestamp:

    def __init__(self, timestamp_raw):
        """A simple class for handling and formatting timestamps"""
        self.raw = timestamp_raw
        self.timestamp = self.formatted_timestamp(timestamp_raw)
        self.datetime = dt.strptime(self.timestamp, "%Y-%m-%d-%H-%M-%S")

    def __repr__(self):
        return self.get_time(self.raw)

    def __str__(self):
        """string representation of Timestamp objects return the raw input variable"""
        return self.get_time(self.raw)

    @staticmethod
    def formatted_timestamp(tsr):
        """Format raw timestamp from logs"""
        return tsr.replace("T", "-").replace(":", "-")

    @staticmethod
    def get_time(timestamp):
        """Returns the time, formatted 00:00 AM/PM"""
        return dt.strptime(':'.join(timestamp.split("T")[1].split(":")[:-1]), "%H:%M").strftime("%I:%M %p")

    @staticmethod
    def get_time_m(timestamp):
        """Returns the time, as military time (m)"""
        return timestamp.split("T")[1]

    @staticmethod
    def get_time_s(timestamp):
        """returns get_time value, but with seconds"""
        return dt.strptime(':'.join(timestamp.split("T")[1].split(":")), "%H:%M:%S").strftime("%I:%M:%S %p")
