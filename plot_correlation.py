import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse


def count_on_dataset(filename, words):
    count = {}

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tweet = row['words'].split(' ')
            date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S').date()
            if date not in count.keys():
                count[date] = [0] * len(words)
            for i in range(len(words)):
                n = set(tweet).intersection(set(words[:i+1]))
                if len(n) == i + 1:
                    count[date][i] += 1

    return count


def main(filename, words):
    count = count_on_dataset(filename, words)

    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    ax1.set_xlabel('Days')
    ax1.set_ylabel('# appearances in tweets')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Interest value')

    for i in range(len(words)):
        x, y, y_int = [], [], []
        for date in count.keys():
            x.append(date)
            y.append(count[date][i])

            if i > 0:
                res = 0
                if count[date][i-1] > 0:
                    res = count[date][i] / count[date][i-1]
                y_int.append(res)

        legend = words[0]
        if i > 0:
            legend = r"({}) $\rightarrow$ {}".format(', '.join(words[:i]), words[i])
        ax1.plot(x, y, label=legend)
        if i > 0:
            ax2.plot(x, y_int, '--', label=legend)

    fig.suptitle('Correlation ({})'.format(', '.join(words)))
    ax1.legend()
    ax2.legend()

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('dataset', type=str, default='dataset.csv',
                        help='the sorted dataset file to work on')
    parser.add_argument('--words', '-w', type=str, nargs='+', required=True,
                        help='list of words in correlation order')

    args = parser.parse_args()
    main(args.dataset, args.words)
