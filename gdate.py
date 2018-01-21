from datetime import datetime, timedelta
from pytz import timezone

EST = timezone('US/Eastern')
gEST = "-05:00"


def get_now():
    return datetime.now(tz = EST)


def datetime_to_gdate(date):
    return date.isoformat()


def gdate_to_datetime(date):
    date = date[:-3] + date[-2:]
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')


def get_midnight(date):
    """
    Returns midnight of the current date. The output datetime will always be before or at the same time as
     the input date.
    :param date:
    :return:
    """
    return datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0, tzinfo=EST)
