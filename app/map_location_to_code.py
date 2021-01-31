# see https://weather.codes/united-kingdom/
# https://github.com/geekinthesticks/python-yahoo-weather/blob/master/uk_locations.org
def map_location_to_code(location):
    """
    Map Location to code
    :param location:
    :return:
    """

    mapping = {
        'Stockcross, UK': 'UKXX0097',
        'Yarmouth Harbour, UK': 'UKXX0795',
        'Lymington Harbour, UK': 'UKXX1414',
        'Portsmouth, UK': 'UKXX0115',
        'Cowes, UK': 'UKXX0707'
    }

    if location in mapping:
        return mapping[location]
    else:
        return 'UNKNOWN'
