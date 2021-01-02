import os


def get_stage():
    if 'STAGE' in os.environ:
        stage = os.environ['STAGE']
    else:
        stage = 'IDE'  # i.e. running in PyCharm
    return stage


def get_version():
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    else:
        version = 'IDE'  # i.e. running in PyCharm

    return version


def get_db_hostname():
    if 'SQL_DB_HOSTNAME' in os.environ:
        hostname = os.environ['SQL_DB_HOSTNAME']
    else:
        hostname = '192.168.1.15'  # my dev machine
    return hostname


def calc_api_calls(num_locations, sleep_secs):
    """
    Calculate number of api calls that will be made per 24 hours
    limit is 1000 per day

    :return:

    >>> calc_api_calls(1, 3600)
    24
    >>> calc_api_calls(2, 600)
    288
    >>> calc_api_calls(3, 600)
    432
    >>> calc_api_calls(4, 600)
    576
    >>> calc_api_calls(5, 600)
    720
    >>> calc_api_calls(6, 600)
    864
    """
    api_calls_per_day = (24 * 3600 * num_locations) / sleep_secs

    return int(api_calls_per_day)
