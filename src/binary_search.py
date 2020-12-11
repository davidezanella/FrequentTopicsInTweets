import os
from io import StringIO
import csv
from datetime import datetime


def load_subset_dataset(filename, day):
    n_bytes = os.stat(filename).st_size
    increment = 20
    dataset = []

    with open(filename, 'r') as file:
        left, right = 0, n_bytes - 1
        key = None
        while key != day.date() and left <= right:
            mid = (left + right) / 2
            file.seek(mid)
            # now realign to a record
            if mid:
                file.readline()
            line = file.readline()
            f = StringIO(line)
            reader = csv.reader(f)
            date = list(reader)[0][0]
            key = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
            if day.date() > key:
                left = mid + increment
            else:
                right = mid - increment
        if key is None:
            return []
        # mid is the position of one element with the desired key
        lines_added = set()
        for direction in [-1, 1]:
            i = 0
            while True:
                pos = mid + (i * increment * direction)
                if pos < 0 or pos > n_bytes:
                    break
                file.seek(pos)
                file.readline()  # to realign the cursor
                if file.tell() not in lines_added:
                    lines_added.add(file.tell())
                    line = file.readline()
                    f = StringIO(line)
                    reader = csv.reader(f)
                    if len(line.strip()) == 0:
                        break
                    row = list(reader)[0]
                    date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    if date.date() != day.date():
                        break
                    dataset.append({
                        'date': date,
                        'words': set(row[1].split(' '))
                    })

                i += 1
    return dataset


def min_and_max_dates_dataset(filename):
    n_bytes = os.stat(filename).st_size
    with open(filename, 'r') as file:
        file.seek(12)
        line = file.readline()

        f = StringIO(line)
        reader = csv.reader(f)
        row = list(reader)[0]
        min_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

        char = ''
        pos = 20
        while char != '\n':
            file.seek(n_bytes - pos)
            char = file.read(1)
            pos += 1
        line = file.readline()
        f = StringIO(line)
        reader = csv.reader(f)
        row = list(reader)[0]
        max_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

    return min_date, max_date
