# Frequent topics in tweets

Project for the Data Mining course @ UniTN 2020/2021.

The purpose of this project is to find, starting from a dataset containing tweets, consistent topics in time. 
A topic is a set of terms, and terms, since we are referring to tweets, are any word present in a Twitter’s post, so even hashtags or usernames. By consistent topics in time, it means topics that, when they become popular, they are
frequently together.

### How to use

To launch the program execute the `main.py` script as follows:
```shell
python3 main.py test_dataset.csv
```
To see all the available parameters use the `--help` command:
```shell
usage: main.py [-h] [--min_confidence MIN_CONFIDENCE] [--days_support DAYS_SUPPORT] dataset

positional arguments:
  dataset               the sorted dataset file to work on

optional arguments:
  -h, --help            show this help message and exit
  --min_confidence MIN_CONFIDENCE
                        minimum value of confidence to be considered [0,1]
  --days_support DAYS_SUPPORT
                        minimum number of days support value
```

The other scripts are described below:
* `create_dataset.py`: using a raw dataset as input creates a new one cleaning it and sorting by dates;
* `plot_correlation.py`: plots the correlation between two or more terms present in the dataset;
* `plot_dataset_statistics.py`: plots the statistics of a dataset showing the distributions of words per tweet, hours and days of the tweets;
* `plot_run_metrics.py`: takes a csv with the metrics of an execution and plots the CPU and memory usage of the process.
