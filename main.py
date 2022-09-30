import os
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv
from web3 import Web3
from versions.halving import halving
from versions.ultra_slow import ultra_slow
from versions.etherscan import etherscan


def main(version="halving"):
    logging.info("Starting script in version %s", version)

    last_blocks = []
    start_date = datetime.strptime(os.getenv("START_DATE"), "%Y-%d-%m").date()
    end_date = datetime.strptime(os.getenv("END_DATE"), "%Y-%d-%m").date()

    w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
    if not w3.isConnected():
        raise Exception("Could not connect to Ethereum node")

    logging.debug("Connected to Ethereum node")

    match version:
        case "ultra_slow":
            start_block = int(os.getenv("INITIAL_BLOCK", default="0"))
            last_blocks = ultra_slow(w3, start_date, end_date, start_block)
        case "halving":
            last_blocks = halving(w3, start_date, end_date)
        case "etherscan":
            last_blocks = etherscan(start_date, end_date)

    print("Last blocks of each day:")
    for day, block in last_blocks:
        print(f"> {day} - {block}")

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('version', type=str, default='halving',
        help='version of the script to run')
    args = parser.parse_args()

    main(args.version)
