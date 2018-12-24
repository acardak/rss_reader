#!/usr/bin/python
# encoding: utf-8

import argparse
import re
import validators
import yaml
from bs4 import BeautifulSoup
from collections import OrderedDict
from six.moves import urllib

CONVERSION_MAP = {
    'ユーザベース': 'UZABASE'
}

TITLE_LENGTH = 10
BODY_LENGTH = 30


def set_encoding():
    import sys
    if sys.version_info < (3,):
        reload(sys)
        sys.setdefaultencoding('utf8')


def trim_spaces(text):
    return ' '.join(text.split())


def extract_articles_from_url(feed_url):
    page = urllib.request.urlopen(feed_url)
    soup = BeautifulSoup(page, 'html.parser')
    all_articles = soup.find_all('article')
    extracted_articles = []
    for article in all_articles:
        article_dic = OrderedDict()
        article_dic['title'] = article.h1.text.strip()
        article_body = []
        for p in article.find_all('p'):
            article_body += [trim_spaces(p.text)]
        article_dic['body'] = ''.join(article_body)
        extracted_articles += [article_dic]
    return extracted_articles


def extract_articles_from_file(file_path):
    with open(file_path, 'rb') as f:
        raw_articles = f.read().decode('utf-8')
    extracted_articles = []
    match_titles = re.finditer('title: (.*)', raw_articles)
    match_bodies = re.finditer('body: (.*)', raw_articles)
    for title, body in zip(match_titles, match_bodies):
        article_dic = OrderedDict()
        article_dic['title'] = title.groups(1)[0]
        article_dic['body'] = body.groups(1)[0]
        extracted_articles += [article_dic]
    return extracted_articles


def extract_articles(article_source):
    if validators.url(article_source):
        extracted_articles = extract_articles_from_url(article_source)
    else:
        extracted_articles = extract_articles_from_file(article_source)
    return extracted_articles


def convert_keywords(articles, conversion_map):
    for article in articles:
        for k, v in conversion_map.items():
            article['body'] = article['body'].replace(k, v)
    return articles


def trim_articles(articles, title_length, body_length):
    for article in articles:
        article['title'] = article['title'][:title_length] + '...'
        article['body'] = article['body'][:body_length] + '...'
    return articles


def format_articles(articles, convert_options, conversion_map, title_length, body_length):
    if convert_options and 'convert' in convert_options.split(','):
        articles = convert_keywords(articles, conversion_map)
    if convert_options and 'cut' in convert_options.split(','):
        articles = trim_articles(articles, title_length, body_length)
    return articles


def print_articles(articles):
    for article in articles:
        print('title: %s' % article['title'])
        print('body: %s' % article['body'])
        print('')


def save_articles(articles, output_file):
    def represent_dictionary_order(self, dict_data):
        return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())
    yaml.add_representer(OrderedDict, represent_dictionary_order)
    with open(output_file, 'w') as f:
        yaml.dump(articles, f, allow_unicode=True, default_flow_style=False)


def process_output(articles, output_file=None):
    if output_file:
        save_articles(articles, output_file)
    else:
        print_articles(articles)


def parse_input_args():
    parser = argparse.ArgumentParser(description='Extract and convert articles')
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-c', '--convert')
    parser.add_argument('-o', '--output')
    return parser.parse_args()


def main():
    parsed_args = parse_input_args()
    article_source = parsed_args.input
    convert_options = parsed_args.convert
    output_file = parsed_args.output

    extracted_articles = extract_articles(article_source)
    formatted_articles = format_articles(extracted_articles, convert_options, CONVERSION_MAP, TITLE_LENGTH, BODY_LENGTH)
    process_output(formatted_articles, output_file)


if __name__ == '__main__':
    set_encoding()
    main()
