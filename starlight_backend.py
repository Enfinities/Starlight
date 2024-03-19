import json
from datetime import datetime
import requests

def read_json(filename):
    """Read all data from a JSON file.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :return: (dict) all the data that was in the JSON file
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    return json_data


def edit_value(filename: str, user_id: int, field: str, new_value):
    """Edit a value for a particular user in the JSON file.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :param user_id: (int) the Discord ID of the person whose information is being updated
    :param field: (str) the name of the field containing the value that is to be updated
    :param new_value: (any) the new value will be placed in the desired field
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data[user_id][field] = new_value

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def initialize_json(filename):
    """Creates the JSON file if there isn't one already.

    :param filename: (str) the name of the JSON file being created (ends with .json)
    """
    birth_time = int(datetime.now().timestamp())
    start_data = {319472632493768705: {'nick': 'Grey',
                                       'leetcode_username': 'tetragrey',
                                       'weekly_quota': 0,
                                       'stars_at_week_start': 0,
                                       'warning_message': "Grey, it looks like you didn't get your stars for this "
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  583730259409633310: {'nick': 'Kat',
                                       'leetcode_username': 'Enfinities',
                                       'weekly_quota': 0,
                                       'stars_at_week_start': 0,
                                       'warning_message': "Kat, it looks like you didn't get your stars for this "
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  309330832047210497: {'nick': 'Anytime',
                                       'leetcode_username': 'MrPositions',
                                       'weekly_quota': 0,
                                       'stars_at_week_start': 0,
                                       'warning_message': "Anytime, it looks like you didn't get your stars for this "
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  1015276712948400148: {'nick': 'Raspberry Kitten',
                                        'leetcode_username': 'Grindelia',
                                        'weekly_quota': 0,
                                        'stars_at_week_start': 0,
                                        'warning_message': "Raspberry Kitten, it looks like you didn't get your stars "
                                                           "for this week...",
                                        'warning_image_url': 'https://tenor.com/view/caulifla-dragon-ball-z-super-'
                                                             'saiyan-gif-15035166'},
                  'birth_time': birth_time
                  }

    with open(filename, 'w') as file:
        json.dump(start_data, file, indent=4)


def get_leetcode_stats(username):
    api_link = f'https://leetcodestats.cyclic.app/{username}'
    response = requests.get(api_link)

    if response.status_code == 200:
        data = response.json()
        stars = 0
        stars += data.get("easySolved", 0) * 1
        stars += data.get("mediumSolved", 0) * 3
        stars += data.get("hardSolved", 0) * 5
        return {
            "username": username,
            "stars": stars,
            "totalSolved": data.get("totalSolved", 0),
            "easySolved": data.get("easySolved", 0),
            "mediumSolved": data.get("mediumSolved", 0),
            "hardSolved": data.get("hardSolved", 0)
        }
    else:
        print(f"Failed to fetch data for user '{username}'")
        return {
            "username": "not found",
            "stars": 0,
            "totalSolved": 0,
            "easySolved": 0,
            "mediumSolved": 0,
            "hardSolved": 0
        }
