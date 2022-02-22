import datetime


def get_aware_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
