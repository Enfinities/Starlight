import asyncio
from datetime import datetime

from starlight_backend import read_json, get_leetcode_stats, edit_value


async def timer_main(filename):
    """Sets the timer to repeat every week. On end of cycle, checks who's been slacking and sends them a warning."""
    check_period = 30 * 60
    while True:
        interval = get_remaining_duration(filename)
        if await timer(interval, check_period) is True:
            json_data = read_json(filename)
            for user_id in [key for key in json_data.keys() if key.isdigit()]:
                leet_stats = get_leetcode_stats(json_data[user_id]['leetcode_username'])
                if not check_slackers(json_data[user_id], leet_stats):
                    warning_message = format_warning(user_id, json_data[user_id], leet_stats)
                    yield warning_message
                    yield json_data[user_id]['warning_image_url']
            cycle_update(filename)
            json_data = read_json(filename)
            yield ("It's the start of a new week! Everyone's stars have been updated. Time to race for that quota! "
                   f"After all, you only have until {json_data['interval_start_time'] + (7 * 24 * 60 * 60)}! ;)")


def get_remaining_duration(filename):
    """Finds the number of remaining seconds in the interval, which is then fed to the timer function.
    This is useful in case bot operation is suspended for some reason.

    :return: (int) the number of seconds remaining before the interval ends
    """
    seconds_in_week = 7 * 24 * 60 * 60
    time_now = int(datetime.now().timestamp())
    json_data = read_json(filename)
    interval_start_time = json_data['interval_start_time']

    remaining_duration = interval_start_time + seconds_in_week - time_now
    return remaining_duration


async def timer(duration, check_period):
    """Counts down from whatever the duration is (in seconds), returns True when the countdown ends.

    :param duration: (int) the number of seconds for each interval. The plan is to make this the number of seconds
    in one week, so that we have intervals of one week
    :param check_period: (int) the number of seconds that will pass between checks to see if the interval has ended.
    """
    timer_countdown = int(duration)
    while True:
        await asyncio.sleep(check_period)
        timer_countdown -= check_period
        print(f'Countdown: {timer_countdown} seconds to next cycle.\n'
              f'The next check will occur in {int(check_period/60)} minutes.')
        if timer_countdown <= 0:
            return True


def check_slackers(user_json_data, user_leet_data):
    total_stars = user_leet_data['stars']
    start_stars = user_json_data['stars_at_week_start']
    quota = user_json_data['weekly_quota']
    if total_stars - start_stars >= quota:
        return True
    else:
        return False


def format_warning(user_id, user_json_data, user_leet_data):
    stars_earned = user_leet_data['stars'] - user_json_data['stars_at_week_start']
    msg = (f"<@{user_id}>...\n``` ```\n"
           f"{user_json_data['warning_message']}\n"
           f"Your record this week:\n"
           f"- Quota: {user_json_data['weekly_quota']}\n"
           f"- Stars earned this week: {stars_earned}\n"
           f"``` ```")
    return msg


def cycle_update(filename):
    """Update all values that need to be updated so the cycle can start anew"""
    # Set the interval start time for the new cycle
    new_interval_start = int(datetime.now().timestamp())
    edit_value(filename, None, 'interval_start_time', new_interval_start)

    # Find total stars and send them into the json as stars_at_week_start
    json_data = read_json(filename)
    for user_id in [key for key in json_data.keys() if key.isdigit()]:
        leet_stats = get_leetcode_stats(json_data[user_id]['leetcode_username'])
        edit_value(filename, user_id, 'stars_at_week_start', leet_stats['stars'])
