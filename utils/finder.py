import logging
from datetime import datetime

class Finder:
    w3 = None
    last_block = None

    checkpoints = {}

    def __init__(self, w3):
        self.w3 = w3
        self.last_block = self.w3.eth.getBlock('latest').number

    def test_find_last_block(self, target_date, start, end):
        return self.__find_last_block(target_date, start, end)

    def find_last_block(self, target_date):
        if len(self.checkpoints) == 0:
            return self.__find_last_block(target_date, 0, self.last_block)

        start = None
        end = None

        sorted_dates = sorted(self.checkpoints.keys())

        if target_date in self.checkpoints:
            start = self.checkpoints[target_date][1]

        for index, value in enumerate(sorted_dates):
            if value > target_date:
                if start is None and index > 0:
                    start = self.checkpoints[sorted_dates[index - 1]][1]
                end = self.checkpoints[value][0]
                break

        if end is None:
            if start is None:
                start = self.checkpoints[sorted_dates[-1]][1]
            end = self.last_block

        if start is None:
            start = 0

        return self.__find_last_block(target_date, start, end)

    def __find_last_block(self, target_date, start, end):
        diff = end - start
        half = diff // 2

        if diff == 0:
            return start
        elif diff == 1:
            end_block = datetime.utcfromtimestamp(self.w3.eth.getBlock(end).timestamp)

            if end_block.date() == target_date:
                return end
            return start

        block = self.w3.eth.getBlock(start + half)
        block_date = datetime.utcfromtimestamp(block.timestamp).date()

        logging.debug("Processing block %s", start + half)

        if block_date not in self.checkpoints:
            self.checkpoints[block_date] = (block.number, block.number)
        elif block_date in self.checkpoints:
            min_block, max_block = self.checkpoints[block_date]

            if block.number < min_block:
                self.checkpoints[block_date] = (block.number, max_block)
            elif block.number > max_block:
                self.checkpoints[block_date] = (min_block, block.number)

        if block_date > target_date:
            return self.__find_last_block(target_date, start, start + half)
        else:
            return self.__find_last_block(target_date, start + half, end)
