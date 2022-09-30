import math
from datetime import datetime, timedelta, timezone
import logging
import requests

def get_last_block(timestamp):
    payload = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": str(timestamp),
        "closest": "before",
        "apikey": "7GG69XKXDY2QKW1942S544PGDUJ1N7IZ51"
    }
    response = requests.get('https://api.etherscan.io/api', params=payload)
    data = response.json()

    return data["result"]


def etherscan(start_date, end_date):
    last_blocks = []

    for n in range(int((end_date - start_date).days)):
        logging.debug("Processing day %s", start_date + timedelta(days=n))

        date = start_date + timedelta(n)
        dt = datetime.combine(date, datetime.max.time(), tzinfo=timezone.utc)
        timestamp = math.trunc(dt.timestamp())

        last_block = get_last_block(timestamp)
        last_blocks.append((date, last_block))

    return last_blocks
