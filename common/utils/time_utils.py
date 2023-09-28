from datetime import datetime


def get_curr_time() -> int:
    curr_time = int(datetime.now().timestamp())
    return curr_time