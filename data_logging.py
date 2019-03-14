
import datetime
import os
import re
from timer_utils import tz
from collections import namedtuple, OrderedDict


file_format = '{title}_{date}_{num}.csv'
regex_file_format = file_format.replace('.','\\.')
folder = 'data'
sep = ','

class FileLogger():
    def __init__(self, title, add_time=True, headers=[]):
        self.title = title
        self.add_time = add_time
        if hasattr(headers, '_fields'):
            self.headers = list(headers._fields)
        else:
            self.headers = headers

    def get_today(self):
        today = datetime.date.today()
        return '{:04d}{:02d}{:02d}'.format(today.year, today.month, today.day)


    def get_new_filename(self):
        today = self.get_today()
        regex_arguments = {'title': self.title, 'date': today, 'num': '([0-9][0-9][0-9])'}
        file_pattern = regex_file_format.format(**regex_arguments)
        largest_number = -1 # start at -1 so when we add one it makes 0
        for f in os.listdir(folder):
            match = re.match(file_pattern, f)
            if match:
                n = int(match.group(1))
                if n > largest_number:
                    largest_number = n
        new_number = largest_number + 1
        return folder + '/' + file_format.format(title=self.title, date=today, num='{:03d}'.format(new_number))

    def log(self, data):
        if isinstance(data, dict):
            if not self.headers:
                print("cant feed dict without headers")
            data_list = [data[i] for i in self.headers]
        elif isinstance(data, list):
            data_list = data
        elif isinstance(data, str):
            data_list = [data]
        elif hasattr(data, '_asdict'):
            data_list = list(data._asdict().values())
        else:
            print('data is unrecognized type')
            return

        if self.add_time:
            now = datetime.datetime.now(tz)
            data_list = [now] + data_list
        line = sep.join(str(i) for i in data_list) + '\n'
        self.file.write(line)
        self.file.flush()
        # location_in_file=self.file.seek(0, 1)
        # print(location_in_file)



    def __enter__(self):
        new_filename = self.get_new_filename()
        print('started logging to', new_filename)
        self.file = open(new_filename, 'a')
        headers_list = []
        if self.headers:
            headers_list = self.headers
        if self.add_time:
            headers_list = ['time'] + headers_list
        if headers_list:
            line = sep.join(headers_list) + '\n'
            self.file.write(line)
        return self


    def __exit__(self, type, value, traceback):
        self.file.close()
        self.file = None

def test():
    with FileLogger('test', headers=['first_column', 'second_column', 'third_column']) as logger:
        logger.log(['first row', 10, True])
        logger.log(dict(first_column='second row', second_column=20, third_column=False))
        logger.log('third row')

if __name__ == '__main__':
    test()