import re
import unicodedata
import glob
import os


def remove_files_in_path(path):
  cur_path = os.getcwd()
  os.chdir(path)
  files = glob.glob("*")
  for file in files:
    os.remove(file)
  os.chdir(cur_path)


def remove_unicode_characters(phrase):
  return unicodedata.normalize('NFKD', phrase.decode('utf-8')).encode('ascii', 'ignore')


def split_words(phrase):
  words = set(re.findall(r"[\w']+", phrase))
  return words


def split_unicode_words(phrase):
  ascii_phrase = remove_unicode_characters(phrase)
  words = split_words(ascii_phrase)
  return words


def get_keys_values_of_dict(dict):
  values = []
  keys = []
  for key, value in dict.items():
    values.append(value)
    keys.append(key)

  return keys, values


def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]
