import re
import unicodedata


def remove_unicode_characters(phrase):
  return unicodedata.normalize('NFKD', phrase.decode('utf-8')).encode('ascii', 'ignore')


def split_words(phrase):
  words = set(re.findall(r"[\w']+", phrase))
  return words


def split_unicode_words(phrase):
  ascii_phrase = remove_unicode_characters(phrase)
  words = split_words(ascii_phrase)
  return words