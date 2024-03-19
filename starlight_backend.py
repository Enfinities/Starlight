import json


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
    start_data = {319472632493768705: {'nick': 'Grey',
                                       'weekly_quota': 0,
                                       'warning_message': "Grey, it looks like you didn't get your stars for this"
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  583730259409633310: {'nick': 'Kat',
                                       'weekly_quota': 0,
                                       'warning_message': "Kat, it looks like you didn't get your stars for this"
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  309330832047210497: {'nick': 'Anytime',
                                       'weekly_quota': 0,
                                       'warning_message': "Anytime, it looks like you didn't get your stars for this"
                                                          "week...",
                                       'warning_image_url': 'https://tenor.com/view/cat-reminder-gif-'
                                                            '8682463232604832341'},
                  1015276712948400148: {'nick': 'Raspberry Kitten',
                                        'weekly_quota': 0,
                                        'warning_message': "Raspberry Kitten, it looks like you didn't get your stars"
                                                           "for this week...",
                                        'warning_image_url': 'https://tenor.com/view/caulifla-dragon-ball-z-super-'
                                                             'saiyan-gif-15035166'}
                  }

    with open(filename, 'w') as file:
        json.dump(start_data, file, indent=4)