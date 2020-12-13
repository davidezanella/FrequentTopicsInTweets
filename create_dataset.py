import csv
import nltk
import re
import string
from csvsort import csvsort
from tqdm import tqdm
import argparse


def get_words(text):
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(text)
    nouns = [word.lower() for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    return nouns


def get_usernames(text):
    return re.findall(r'@\S+', text)


def get_hashtags(text):
    return re.findall(r'#\S+', text)


def remove_urls(text):
    return re.sub(r'http\S+', '', text)
    

def remove_emoji(text):
    emoji_pattern = re.compile('[^' + ''.join(string.printable) + ']')
    return emoji_pattern.sub(r'', text)


def remove_punctuation(text):
    return re.sub(r'[\,\.:;…~|"”“\(\)\[\]%]', ' ', text)


def main(input_file):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    output_file = 'dataset_{}'.format(input_file)

    with open(input_file) as csvfile:
        reader = csv.DictReader(csvfile)

        with open(output_file, 'w') as csvoutput:
            writer = csv.DictWriter(csvoutput, fieldnames=['date', 'words'])
            writer.writeheader()

            for row in tqdm(reader):
                if row['text'] is not None:
                    text = remove_urls(row['text'])
                    text = remove_emoji(text)
                    text = remove_punctuation(text)
                    usernames = get_usernames(text)
                    hashtags = get_hashtags(text)
                    # remove the username from the tweet
                    text = ' '.join([word for word in text.split() if word not in usernames + hashtags])
                    words = ' '.join(hashtags + usernames + get_words(text))
                    if len(words) > 0:
                        writer.writerow({
                            'date': row['date'],
                            'words': words
                        })

    csvsort(output_file, [0], output_filename='sorted_dataset_' + input_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('dataset', type=str, default='dataset.csv',
                        help='the input dataset file to work on')

    args = parser.parse_args()
    main(args.dataset)
