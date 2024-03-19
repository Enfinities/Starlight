import asyncio
from starlight_backend import read_json, get_leetcode_stats


async def timer_main(filename):
    """Sets the timer to repeat every week. On end of cycle, checks who's been slacking and sends them a warning."""
    seconds = 7 * 24 * 60 * 60
    check_period = 30 * 60
    while True:
        if await timer(seconds, check_period) is True:
            json_data = read_json(filename)
            for user_id in [key for key in json_data.keys() if isinstance(key, int)]:
                leet_stats = get_leetcode_stats(json_data[user_id]['leetcode_username'])
                if not check_slackers(json_data[user_id], leet_stats):
                    warning_message = format_warning(json_data[user_id], leet_stats)
                    yield warning_message


async def timer(duration, check_period):
    """Counts down from whatever the duration is (in seconds), returns True when the countdown ends.

    :param duration: (int) the number of seconds for each interval. The plan is to make this the number of seconds
    in one week, so that we haev intervales of one week
    :param check_period: (int) the number of seconds that will pass between checks to see if the interval has ended.
    """
    timer_countdown = int(duration)
    while True:
        await asyncio.sleep(check_period)
        timer_countdown -= check_period
        if timer_countdown <= 0:
            print(f'test {timer_countdown}')
            return True


def snapshot():
    pass


def check_slackers():
    pass


def format_warning():
    msg = (f"``` ```"
           f"Username: {leet_name}\n- Stars: {stats['stars']}\n"
           f"- Stars This Week: {stars_at_week_start - stats['stars']}"
           f"- Weekly Star Quota: {weekly_quota}"
           f"- Total Solved: {stats['totalSolved']}\n"
           f"- Easy Solved: {stats['easySolved']}\n- Medium Solved: {stats['mediumSolved']}\n"
           f"- Hard Solved: {stats['hardSolved']}\n"
           f"- Warning Message: {warning_message}\n"
           f"- Warning Image: {warning_image}\n"
           f"``` ```"
    return ''
