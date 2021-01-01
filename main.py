from datetime import timedelta
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count
import functools
from tqdm import tqdm
import argparse
import json

from src.elaborate_baskets import BasketWorker
from src.binary_search import load_subset_dataset, min_and_max_dates_dataset


def start_process(filename, min_confidence, day):
    basket = load_subset_dataset(filename, day)
    worker = BasketWorker(basket, min_confidence)
    return worker()


def find_frequency_in_time(baskets_result):
    count = {}
    for basket in baskets_result:
        for key in basket.keys():
            val = count.get(key, (0, 0))
            count[key] = (val[0] + 1, val[1] + basket[key].confidence)

    count = sorted(count.items(), key=lambda x: x[1][1]/x[1][0], reverse=True)
    return count


def main(filename, min_confidence):
    first_day, last_day = min_and_max_dates_dataset(filename)
    num_days = (last_day.date() - first_day.date()).days + 1
    date_list = [first_day + timedelta(days=x) for x in range(num_days)]
    print("first day:", first_day.date())
    print("last day:", last_day.date())

    start = timer()
    print(f'starting computations on {cpu_count()} cores')

    with Pool() as pool:
        start_process_fn = functools.partial(start_process, filename, min_confidence)
        res = list(tqdm(pool.imap(start_process_fn, date_list), total=len(date_list)))

    res = list(res)

    end = timer()
    print(f'elapsed time: {end - start}')

    most_freq = find_frequency_in_time(res)
    most_freq = list(filter(lambda x: len(x[0]) > 1, most_freq))

    results = {
        'dataset': filename,
        'min_confidence': min_confidence,
        'time': end - start,
        'results': [{
            'set': val[0],
            'days_of_popularity': val[1][0],
            'mean_confidence': val[1][1]/val[1][0]
        } for val in most_freq]
    }

    with open(filename + '_results.json', 'w') as outfile:
        json.dump(results, outfile)

    for i, val in enumerate(most_freq[:20]):
        print('{} -> {}, days of popularity: {}, mean confidence: {}'.format(i+1, val[0], val[1][0], val[1][1]/val[1][0]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('dataset', type=str, default='dataset.csv',
                        help='the sorted dataset file to work on')
    parser.add_argument('--min_confidence', type=float, default=0.7,
                        help='minimum value of confidence to be considered [0,1]')

    args = parser.parse_args()
    main(args.dataset, args.min_confidence)
