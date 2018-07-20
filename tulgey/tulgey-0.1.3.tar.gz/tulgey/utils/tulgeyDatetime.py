from datetime import datetime

DATETIME_FORMAT = "%Y %m %d %H %M %S"


def toString(datetime: datetime) -> str:
    return datetime.strftime(DATETIME_FORMAT)


def fromString(dateStr: str) -> datetime:
    return datetime.strptime(dateStr, DATETIME_FORMAT)
