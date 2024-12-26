import time


def is_even_with_sleep(number: int) -> bool:
    time.sleep(0.05)
    return number % 2 == 0
