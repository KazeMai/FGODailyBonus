from datetime import datetime, timedelta, timezone

tz_utc_8 = timezone(timedelta(hours=8))
tz_utc_9 = timezone(timedelta(hours=9))

def GetNowTimeHour():
    return datetime.now(tz=tz_utc_8).hour

def IsDaySame(timestamp):
    tmptime = datetime.fromtimestamp(timestamp).replace(tzinfo=tz_utc_9)
    nowtime = datetime.now(tz=tz_utc_9)
    if tmptime.day == nowtime.day and tmptime.month == nowtime.month and tmptime.year == nowtime.year :
        return True
    else :
        return False


def GetNowTime():
    return datetime.now(tz=tz_utc_8)


def GetFormattedNowTime():
    return datetime.now(tz=tz_utc_8).strftime('%Y-%m-%d %H:%M:%S')


def GetTimeStamp():
    return (int)(datetime.now(tz=tz_utc_8).timestamp())


def TimeStampToString(timestamp):
    return datetime.fromtimestamp(timestamp)


def GetNowTimeFileName():
    return datetime.now(tz=tz_utc_8).strftime('%Y/%m/%d.log')