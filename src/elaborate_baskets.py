import os
import numpy as np
import matplotlib.pyplot as plt


class BasketWorker:
    def __init__(self, basket, min_interest):
        self.basket = basket
        self.min_interest = min_interest
        self.count = {}

    def __call__(self, *args, **kwargs):
        allowed_words = None
        tweets_idx = None
        tuple_count = {}

        all_counts = {}
        deep = 1
        while True:
            tuple_count, allowed_words, tweets_idx = self.count_deeply(allowed_words, deep, tweets_idx, tuple_count)
            all_counts.update(tuple_count)
            if len(tuple_count.keys()) == 0:
                break
            deep += 1
        return all_counts

    def count_deeply_rec(self, words, keys, tweet_idx):
        if len(keys) == 0:
            keys = [[]]
        for key in keys:
            if len(words.intersection(set(key))) < len(key):
                continue
            for w in words.difference(set(key)):
                new_key = tuple(list(key) + [w])
                status = self.count.get(new_key, SetStatus())
                status.rows.append(tweet_idx)
                status.support += 1
                self.count[new_key] = status

    def count_deeply(self, allowed_words, deep, tweets_idx, old_count):
        self.count = {}

        iterator = tweets_idx
        if iterator is None:
            iterator = range(len(self.basket))
        for idx in iterator:
            useful_words = self.basket[idx]['words']
            if allowed_words is not None:
                useful_words = useful_words.intersection(allowed_words)
            if len(useful_words) >= deep:
                self.count_deeply_rec(useful_words, old_count.keys(), idx)

        support_threshold = 0
        if len(self.count) > 0:
            support_threshold = self.get_min_support()

        # remove keys with support less than support_threshold
        for key, status in list(self.count.items()):
            if status.support < support_threshold:
                del self.count[key]

        if len(old_count) > 0:
            # compute the interest of every association
            for key, status in list(self.count.items()):
                i = key[:-1]
                status.interest = (status.support / old_count[i].support)
                if status.interest < self.min_interest:
                    del self.count[key]

            interests = sorted(self.count.items(), key=lambda x: x[1].interest, reverse=True)
        else:
            interests = sorted(self.count.items(), key=lambda x: x[1].support, reverse=True)

        # print("Process:", os.getpid())
        # print("Deep:", deep)
        # print("Length:", len(self.count.keys()))
        # print("Top 5 interests:", [(i[0], i[1].support, i[1].interest) for i in interests[:5]])

        all_words = set([word for key in self.count.keys() for word in key])
        tweets_idx = set([idx for val in self.count.values() for idx in val.rows])

        return self.count.copy(), all_words, tweets_idx

    def get_min_support(self):
        supports = list(map(lambda x: x.support, self.count.values()))
        supports = list(sorted(supports))
        wall = self.clustering(supports)

        # to remove avoid keeping only outliers
        if len(supports[wall:]) < 3:
            wall = self.clustering(supports[:wall])

        min_support = supports[wall]

        return min_support

    def clustering(self, supports):
        wall = len(supports) - 1
        stop = False
        while not stop:
            low_centroid = np.mean(supports[:wall])
            high_centroid = np.mean(supports[wall:])
            new_wall = wall
            if abs(low_centroid-supports[wall-1]) < abs(high_centroid-supports[wall-1]):
                new_wall += 1
            if abs(low_centroid-supports[wall]) > abs(high_centroid-supports[wall]):
                new_wall -= 1
            stop = (wall == new_wall)
            wall = new_wall

        return wall


class SetStatus:
    __slots__ = ['support', 'rows', 'interest']

    def __init__(self):
        self.support = 0
        self.rows = []
        self.interest = 0

    def __str__(self):
        return '{} - {}'.format(self.support, self.interest)
