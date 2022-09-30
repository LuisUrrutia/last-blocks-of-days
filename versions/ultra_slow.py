import logging
from datetime import datetime

def ultra_slow(w3, start_date, end_date, start_block=0):
    last_blocks = []

    current_proceessed_block = start_block
    current_processed_day = start_date
    while current_processed_day < end_date:
        logging.debug("Processing block %s", current_proceessed_block)

        block = w3.eth.getBlock(current_proceessed_block)
        block_date = datetime.utcfromtimestamp(block.timestamp).date()

        if block_date > current_processed_day:
            logging.debug("Found block %s for day %s", \
                (current_proceessed_block - 1), current_processed_day)

            last_blocks.append((current_processed_day, current_proceessed_block - 1))
            current_processed_day = block_date
            break

        current_proceessed_block += 1

    return last_blocks
