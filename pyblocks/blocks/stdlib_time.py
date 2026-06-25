from pyblocks.blocks.definition import block

# ── Time Module ──────────────────────────────────────────────────────────

@block(label="time.sleep({seconds})", category="Time", color="#89dceb")
def tm_sleep(seconds):
    return f"time.sleep({seconds})"


@block(label="{result} = time.time()", category="Time", color="#89dceb",
       description="Get the current time in seconds since the epoch.")
def tm_time(result):
    return f"{result} = time.time()"


@block(label="{result} = time.monotonic()", category="Time", color="#89dceb")
def tm_monotonic(result):
    return f"{result} = time.monotonic()"


@block(label="{result} = time.perf_counter()", category="Time", color="#89dceb")
def tm_perf_counter(result):
    return f"{result} = time.perf_counter()"


@block(label="{result} = time.localtime()", category="Time", color="#89dceb")
def tm_localtime(result):
    return f"{result} = time.localtime()"


@block(label="{result} = time.gmtime()", category="Time", color="#89dceb")
def tm_gmtime(result):
    return f"{result} = time.gmtime()"


@block(label="{result} = time.strftime({fmt}, {t})", category="Time", color="#89dceb",
       description="Format a time tuple as a string.")
def tm_strftime(result, fmt, t):
    return f'{result} = time.strftime({fmt}, {t})'


@block(label="{result} = time.strptime({s}, {fmt})", category="Time", color="#89dceb",
       description="Parse a time string according to a format.")
def tm_strptime(result, s, fmt):
    return f'{result} = time.strptime({s}, {fmt})'


@block(label="{result} = time.mktime({t})", category="Time", color="#89dceb",
       description="Convert a time tuple to seconds since the epoch.")
def tm_mktime(result, t):
    return f"{result} = time.mktime({t})"


@block(label="{result} = time.ctime()", category="Time", color="#89dceb",
       description="Get the current time as a human-readable string.")
def tm_ctime(result):
    return f"{result} = time.ctime()"


# ── DateTime Module ──────────────────────────────────────────────────────

@block(label="{result} = datetime.date.today()", category="DateTime", color="#89dceb")
def dt_date_today(result):
    return f"{result} = datetime.date.today()"


@block(label="{result} = datetime.datetime.now()", category="DateTime", color="#89dceb")
def dt_datetime_now(result):
    return f"{result} = datetime.datetime.now()"


@block(label="{result} = datetime.datetime.utcnow()", category="DateTime", color="#89dceb")
def dt_datetime_utcnow(result):
    return f"{result} = datetime.datetime.utcnow()"


@block(label="{result} = datetime.datetime({year}, {month}, {day}, {hour}, {minute}, {second})", category="DateTime", color="#89dceb")
def dt_datetime_new(result, year, month, day, hour, minute, second):
    return f"{result} = datetime.datetime({year}, {month}, {day}, {hour}, {minute}, {second})"


@block(label="{result} = datetime.date({year}, {month}, {day})", category="DateTime", color="#89dceb")
def dt_date_new(result, year, month, day):
    return f"{result} = datetime.date({year}, {month}, {day})"


@block(label="{result} = datetime.timedelta(days={days}, hours={hours}, minutes={minutes}, seconds={seconds})", category="DateTime", color="#89dceb")
def dt_timedelta(result, days, hours, minutes, seconds):
    return f"{result} = datetime.timedelta(days={days}, hours={hours}, minutes={minutes}, seconds={seconds})"


@block(label="{result} = datetime.datetime.strptime({s}, {fmt})", category="DateTime", color="#89dceb",
       description="Parse a date/time string into a datetime object.")
def dt_strptime(result, s, fmt):
    return f'{result} = datetime.datetime.strptime({s}, {fmt})'


@block(label="{result} = {dt}.strftime({fmt})", category="DateTime", color="#89dceb",
       description="Format a datetime object as a string.")
def dt_strftime(result, dt, fmt):
    return f'{result} = {dt}.strftime({fmt})'


@block(label="{result} = {dt}.isoformat()", category="DateTime", color="#89dceb",
       description="Get the datetime as an ISO 8601 formatted string.")
def dt_isoformat(result, dt):
    return f"{result} = {dt}.isoformat()"


@block(label="{result} = {dt}.date()", category="DateTime", color="#89dceb",
       description="Extract the date portion from a datetime object.")
def dt_date(result, dt):
    return f"{result} = {dt}.date()"


@block(label="{result} = {dt}.time()", category="DateTime", color="#89dceb",
       description="Extract the time portion from a datetime object.")
def dt_time(result, dt):
    return f"{result} = {dt}.time()"


@block(label="{result} = {dt}.year", category="DateTime", color="#89dceb")
def dt_year(result, dt):
    return f"{result} = {dt}.year"


@block(label="{result} = {dt}.month", category="DateTime", color="#89dceb")
def dt_month(result, dt):
    return f"{result} = {dt}.month"


@block(label="{result} = {dt}.day", category="DateTime", color="#89dceb")
def dt_day(result, dt):
    return f"{result} = {dt}.day"


@block(label="{result} = {dt}.hour", category="DateTime", color="#89dceb")
def dt_hour(result, dt):
    return f"{result} = {dt}.hour"


@block(label="{result} = {dt}.minute", category="DateTime", color="#89dceb")
def dt_minute(result, dt):
    return f"{result} = {dt}.minute"


@block(label="{result} = {dt}.second", category="DateTime", color="#89dceb")
def dt_second(result, dt):
    return f"{result} = {dt}.second"


@block(label="{result} = {dt}.weekday()", category="DateTime", color="#89dceb",
       description="Get day of week (0=Monday, 6=Sunday).")
def dt_weekday(result, dt):
    return f"{result} = {dt}.weekday()"
