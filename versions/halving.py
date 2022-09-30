import logging
from datetime import timedelta
from utils.finder import Finder

def halving(w3, start_date, end_date):
    last_blocks = []

    finder = Finder(w3)
    for n in range(int((end_date - start_date).days)):
        logging.debug("Processing day %s", start_date + timedelta(days=n))

        date = start_date + timedelta(n)
        last_block = finder.find_last_block(date)
        last_blocks.append((date, last_block))

    return last_blocks
