import csv
import datetime as dt
import re

from .settings import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:
    def __init__(self):
        self.RESULT_PATH = BASE_DIR / 'results'
        self.RESULT_PATH.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_dict = {'status': 'quantity'}
        self.total = 0

    def process_item(self, item, spider):
        pattern = r'\w*.(?P<number>\d+)...(?P<name>.*)'
        name_match = re.search(pattern, item['name'])
        item['number'], item['name'] = name_match.groups()
        self.status_dict.setdefault(item['status'], 0)
        self.status_dict[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = self.RESULT_PATH / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(self.status_dict.items())
            total = ('Total', self.total)
            writer.writerow(total)
