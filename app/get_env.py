# environment
import os


def get_version():
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    else:
        version = 'IDE'  # i.e. running in PyCharm

    return version


def get_stage():
    if 'STAGE' in os.environ:
        stage = os.environ['STAGE']
    else:
        stage = 'IDE'  # i.e. running in PyCharm

    return stage



