
import datetime
import os
import re

file_format = '{title}_{date}_{num}.csv'
regex_file_format = file_format.replace('.','\\.')
folder = 'data'
sep = ','

class FileLogger():
    def __init__(self, title, headers=[]):
        self.title = title
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
        else:
            print('data is unrecognized type')
            return

        line = sep.join(str(i) for i in data_list) + '\n'
        self.file.write(line)



    def __enter__(self):
        new_filename = self.get_new_filename()
        print('started logging to', new_filename)
        self.file = open(new_filename, 'a')
        if self.headers:
            line = sep.join(self.headers) + '\n'
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