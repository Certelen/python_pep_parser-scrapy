import csv
import datetime as dt
import re

from .settings import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:
    def __init__(self):
        self.RESULT_PATH = BASE_DIR / 'results'
        self.RESULT_PATH.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_dict = {}

    def process_item(self, item, spider):
        self.status_dict.setdefault(item['status'], 0)
        self.status_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = self.RESULT_PATH / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            first_row = {'status': 'quantity'}
            total = sum(list(map(int, self.status_dict.values())))
            total = ('Total', total)
            writer = csv.writer(f, dialect='unix')
            writer.writerow(first_row)
            writer.writerows(self.status_dict.items())
            writer.writerow(total)
