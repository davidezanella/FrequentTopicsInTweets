import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse


def collect_metrics(filename):
    x = []
    y_cpu = []
    y_mem = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x.append(datetime.strptime(row['Time'][-8:], '%H:%M:%S'))
            y_cpu.append(float(row['CPU']))
            y_mem.append(float(row['Memory']))

    x_min = x[0]
    x = [(i - x_min).seconds for i in x]

    return x, y_cpu, y_mem


def main(filenames, labels):
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    ax1.set_xlabel('Time (sec)')
    ax1.set_ylabel('% CPU usage')
    ax2.set_xlabel('Time (sec)')
    ax2.set_ylabel('% memory used')

    for i, f in enumerate(filenames):
        x, y_cpu, y_mem = collect_metrics(f)

        ax1.plot(x, y_cpu, label=labels[i])
        ax2.plot(x, y_mem, label=labels[i])

    fig.suptitle('')
    ax1.legend()
    ax2.legend()

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('csv_files', type=str, nargs='+', default='metrics.csv',
                        help='the CSV files containing the saved metrics')
    parser.add_argument('--labels', type=str, nargs='+', required=True,
                        help='the labels corresponding to the metrics files')

    args = parser.parse_args()
    main(args.csv_files, args.labels)
