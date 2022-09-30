# Last block of days

This is collection of scripts that will show you the last block of days in a range.

## Requirements
* Python 3.10 or higher
* Install requirements with `pip install -r requirements.txt`

## Full blockchain

This versions connects directly to the blockchain in order to get the information that we need.

### Ultra slow version

This version is very slow, but it is very easy to understand. It iterates over each block on the blockchain and checks if it is in the range and if it is the last block of the day it stores it on a list to later on print it.

> WARNING: This script will take a long, long, looooong time to run. And it will use a lot of request of the API.

```bash
python main.py ultra_slow
```

This script can be modified to search from the latest block to the oldest block and then sort the list, but it will still take a long time to run. It can also be modified to start from an specific block configuring the `INITIAL_BLOCK` env var, but again, it will still take a long time to run.

### Halving version

This version is faster, and it halves the ranges of blocks to search in each iteration until it finds the last block of the day.
It also manages a checkpoint list where it stores the minimal and maximum block number that is found in this process of halving in order to reduce the range of search for next dates.

```bash
python main.py halving
```

## Non-Blockchain

### Etherscan

Etherscan provides an API to get the information of the blocks. This version uses this API to get the closest block to the date that we are looking for.

```bash
python main.py etherscan
```