
import re
from datetime import datetime, timedelta
def parse_shift(text):
    if not text:
        return None
    elif("-" not in text):
       return None
    text = text.replace(" ", "")
    start_raw, end_raw = map(striptime, text.split("-"))

    if(end_raw=="??"):
      end_raw=start_raw+1
    candidates = []

    # Case 1: both are daytime (e.g. 4-12)
    candidates.append((start_raw, end_raw))

    # Case 2: afternoon start
    candidates.append((start_raw + 12, end_raw + 12))

    # Case 3: overnight shift (e.g. 4-12 → 16-24)
    candidates.append((start_raw + 12, end_raw))
    candidates.append((start_raw, end_raw + 12))

    for start, end in candidates:
        if start >= 6 and end <= 24:
            if end > start:
                return start, end

    return None

def parse_day(text):
    if not text:
        return
    text = text.replace(" ", "")
    date_raw = stripdate(text)
    return date_raw

def build_datetimes(date, shift):
    if not shift:
        return
    start, end = shift
    start_dt = date.replace(hour=int(start), minute=int(start*60)%60)
    if 0 < end <= 23:
      end_dt = date.replace(hour=int(end), minute=int(end*60)%60)
    elif end > 23:
      end_dt = date + timedelta(days=1)
    return start_dt, end_dt

def is_date(text):
    return bool(re.search(r"\d", text))
def striptime(time_string):
  datetime_obj=None
  if ':' in time_string:
    datetime_obj = datetime.strptime(time_string, '%H:%M')
  elif(bool(re.search(r"\d", time_string))):
    datetime_obj=datetime.strptime(time_string, '%H')
  else:
    return time_string
  if(datetime_obj is not None):
    #print(time_string)
    total_mins = (datetime_obj.hour * 60) + datetime_obj.minute
    time_in_hours = total_mins / 60
    return time_in_hours
  print(time_string)
  return datetime_obj

def stripdate(date_string):
  datetime_obj=datetime.strptime(date_string, '%d-%b')
  #print(datetime.today().year, datetime_obj.month, datetime_obj.day)
  #print(datetime(datetime.today().year, datetime_obj.month, datetime_obj.day))
  if(datetime.today()-datetime(datetime.today().year, datetime_obj.month, datetime_obj.day)>timedelta(weeks=40)):
    datetime_obj=datetime_obj.replace(year=datetime.today().year+1)
  else:
    datetime_obj=datetime_obj.replace(year=datetime.today().year)
  return datetime_obj