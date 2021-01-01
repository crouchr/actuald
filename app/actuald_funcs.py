import os

def get_stage():
    if 'STAGE' in os.environ:
        stage = os.environ['STAGE']
    else:
        stage = 'IDE'  # i.e. running in PyCharm
    return stage