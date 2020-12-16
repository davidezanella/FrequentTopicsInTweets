import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse


def count_on_dataset(filename):
    count_days = {}
    count_hours = {}
    count_words = {}
    lines = 0

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tweet = row['words'].split(' ')
            date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
            day = date.date()
            hour = date.hour
            n_words = len(tweet)

            count_days[day] = count_days.get(day, 0) + 1
            count_hours[hour] = count_hours.get(hour, 0) + 1
            count_words[n_words] = count_words.get(n_words, 0) + 1

            lines += 1
    print("Number of tweets:", lines)
    return count_days, count_hours, count_words


def main(filename):
    count_days, count_hours, count_words = count_on_dataset(filename)

    first_day = min(count_days.keys())
    last_day = max(count_days.keys())
    num_days = (last_day - first_day).days + 1

    dates = [first_day + timedelta(days=x) for x in range(0, num_days)]
    height = [count_days.get(d, 0) for d in dates]
    plt.bar(dates, height, align='center')

    plt.xlabel('Days')
    plt.ylabel('# of tweets')
    plt.title('Number of tweets per day')
    plt.xticks(rotation=25)
    plt.tight_layout()

    plt.show()

    plt.bar(count_hours.keys(), count_hours.values())

    plt.xlabel('Hours')
    plt.ylabel('# of tweets')
    plt.title('Number of tweets per hour')

    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    plt.show()

    plt.bar(count_words.keys(), count_words.values())

    plt.xlabel('# of words')
    plt.ylabel('# of tweets')
    plt.title('Number of words in tweets')

    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('dataset', type=str, default='dataset.csv',
                        help='the sorted dataset file to work on')

    args = parser.parse_args()
    main(args.dataset)
