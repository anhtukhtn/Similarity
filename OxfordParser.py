__author__ = 'tu'

#!/usr/bin/env python
# -*- coding: utf-8 -

import xml.etree.ElementTree as ET
import csv
import copy
from collections import OrderedDict

__filename_ox_dict__ = "OxfordXML/B_150107.xml"


def remove_tv(element):
  for sub_element in element:
    if sub_element.tag == "txt_v_s_srf":
      element.remove(sub_element)
    remove_tv(sub_element)


def get_string_of_d_elemnt(element):
#  s = element.text or ""
#  for sub_element in element:
#    if sub_element.tag == "xr":
#      for sub_sub_element in sub_element:
#        if sub_sub_element.tag == "xh" and sub_sub_element.text != None:
#          s += sub_sub_element.text
#    if sub_element.tag == "dh" and sub_element.text != None:
#      s += sub_element.text
#  s += element.tail or ""
  element = copy.deepcopy(element)
  remove_tv(element)
  s = ''.join(element.itertext()) or ""
  s = s[:-1]
  return s


def readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,level):

  # if len(meanings) == 0:
  #   return

  meaning = meanings

  if isinstance(meanings,list):
    meaning = meanings[iMeaning]

  d = meaning.find('.//d') or meaning.find('.//ud');
  if d == None:
    return

  # get meaning
  vn = meaning.find('.//meaning');
  if vn == None:
    vn = meaning.find('.//txt_v_s_srf');

  if vn == None:
    return

  oxfordNouns[runhd][str(iMeaning)] = OrderedDict();

  meaning = meanings[iMeaning]
  if level == 0:
    meaning = meanings;

  # get sd
  sd = meaning.find('.//sd');
  if sd != None:
    oxfordNouns[runhd][str(iMeaning)]['sd'] = sd.text;

  # get d
  d = meaning.find('.//d') or meaning.find('.//ud');
  if d != None:
    d_string = get_string_of_d_elemnt(d)
    oxfordNouns[runhd][str(iMeaning)]['d'] = d_string

  # get meaning
  vn = meaning.find('.//meaning');
  if vn == None:
    vn = meaning.find('.//txt_v_s_srf');
  if vn != None and vn.text != None:
    oxfordNouns[runhd][str(iMeaning)]['tv'] = vn.text;
  elif vn != None and vn.tail != None:
    oxfordNouns[runhd][str(iMeaning)]['tv'] = vn.tail;

  # get examples
  x = meaning.findall('.//x');
  for i in range(len(x)):
    oxfordNouns[runhd][str(iMeaning)]['x' + str(i)] = x[i].text;

  # get see also/async
  xh = meaning.findall('.//xh');
  for i in range(len(xh)):
    oxfordNouns[runhd][str(iMeaning)]['xh' + str(i)] = xh[i].text;

def checkAndRemoveInvalidElement(meanings):

  if not isinstance(meanings,list):
    return meanings

  hasInvalid = 1

  while hasInvalid == 1:
    hasInvalid = 0
    for meaning in meanings:
      d = meaning.find('.//d') or meaning.find('.//ud');
        # get meaning
      vn = meaning.find('.//meaning');
      if vn == None:
        vn = meaning.find('.//txt_v_s_srf');

      if vn == None or d == None or d.text == None:
        meanings.remove(meaning)
        hasInvalid = 1

  return meanings



####################################################################################################
#
# @brief:   read nouns from oxford
#
# @ return: dictionary of nouns
#
def readOxfordNouns():

  oxfordNouns = OrderedDict();

  tree = ET.parse(__filename_ox_dict__);
  root = tree.getroot();

  # get all words
  for word in root.findall('entry'):

    # get word
    runhd = word.find('.//runhd');
    if runhd == None:
      continue

    if runhd.text == "bayou" or runhd.text == "beak"\
        or runhd.text == "beano" or runhd.text == "beast" \
        or runhd.text == "basque" or runhd.text == "batman" or runhd == "bauxite"\
        or runhd.text == "beachwear" or runhd.text == "beano"\
        or runhd.text == "bellwether" or runhd.text == "bergamot"\
        or runhd.text == "biddy" or runhd.text == "billow"\
        or runhd.text == "billy" or runhd.text == "backhander"\
        or runhd.text == "blinder" or runhd.text == "basis"\
        or runhd.text == "blubber" or runhd.text == "blue" \
        or runhd.text == "bogie" or runhd.text == "bounce"\
        or runhd.text == "bounds" or runhd.text == "bourbon"\
        or runhd.text == "bream" or runhd.text == "bullock":
      continue

    # print runhd.text

    runhd = runhd.text;

    # if runhd == 'baccy':
    #   print "holy -----------"
    #   adsf = 1;

    if oxfordNouns.has_key(runhd):
      continue

    # get noun, verb of word
    findallpg = word.findall('.//p-g');
    if len(findallpg) != 0:
      for word_POS in findallpg:
        # get POS
        if word_POS.find('.//z_p_in_p-g') == None:
          continue

        POS = word_POS.find('.//z_p_in_p-g').text;

        if POS.strip() == 'noun':
          meanings = word_POS.findall('.//n-g');


          if len(meanings) != 0:
            oxfordNouns[runhd] = OrderedDict();
            meanings = checkAndRemoveInvalidElement(meanings)
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            break
          else:
            meanings = word_POS.findall('.//d');
            if len(meanings)!= 0 and not oxfordNouns.has_key(runhd):
              oxfordNouns[runhd] = OrderedDict();
              word_POS = checkAndRemoveInvalidElement(word_POS)
              readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
              break
    else:
      POS = word.find('.//z_p');
      if POS != None:
        if POS.text.strip() == 'noun':
          meanings = word.findall('.//sd-g') or word.findall('.//n-g');

          if len(meanings) != 0:
            oxfordNouns[runhd] = OrderedDict();
            meanings = checkAndRemoveInvalidElement(meanings)
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            word = checkAndRemoveInvalidElement(word)
            if len(word) != 0 and not oxfordNouns.has_key(runhd):
              oxfordNouns[runhd] = OrderedDict();
              readContentOfWord(oxfordNouns,runhd,0,word,0);

    for word_2 in word.findall('.//entry'):

      # get word
      runhd = word_2.find('.//runhd');
      if runhd == None:
        continue

      runhd = runhd.text;

      # if runhd == 'ballpark':
      #   adsf = 1;

      # get noun, verb of word
      findallpg = word_2.findall('.//p-g');
      if len(findallpg) != 0:
        for word_POS in findallpg:
          # get POS
          if word_POS.find('.//z_p_in_p-g') == None:
            continue

          POS = word_POS.find('.//z_p_in_p-g').text;

          if POS.strip() == 'noun':
            meanings = word_POS.findall('.//n-g');


            if len(meanings) != 0:
              oxfordNouns[runhd] = OrderedDict();
              meanings = checkAndRemoveInvalidElement(meanings)
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
              break
            else:
              meanings = word_POS.findall('.//d')or word_POS.findall('.//ud');
              meanings = checkAndRemoveInvalidElement(meanings)
              if len(meanings)!= 0 and not oxfordNouns.has_key(runhd):
                oxfordNouns[runhd] = OrderedDict();
                readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
                break
      else:
        POS = word_2.find('.//z_p');
        if POS != None:
          if POS.text.strip() == 'noun':

            meanings = word_2.findall('.//sd-g') or word_2.findall('.//n-g');

            if len(meanings) != 0:
              oxfordNouns[runhd] = OrderedDict();
              meanings = checkAndRemoveInvalidElement(meanings)
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              word_2 = checkAndRemoveInvalidElement(word_2)
              if len(word_2) != 0 and not oxfordNouns.has_key(runhd):
                oxfordNouns[runhd] = OrderedDict();
                readContentOfWord(oxfordNouns,runhd,0,word_2,0);

  ########################################
  return oxfordNouns;
  ########################################

####################################################################################################
#
# @brief:   read nouns from oxford
#
# @ return: dictionary of nouns
#
def readOxfordVerbs():

  oxfordNouns = OrderedDict();

  tree = ET.parse(__filename_ox_dict__);
  root = tree.getroot();

  # get all words
  for word in root.findall('entry') or root.findall('hd') or root.findall('entry/hd'):

    # get word
    runhd = word.find('.//runhd');
    if runhd == None:
      continue

    print runhd.text

    runhd = runhd.text;

    if runhd == 'beloved':
      adsf = 1;

    # get noun, verb of word
    findallpg = word.findall('.//p-g');
    if len(findallpg) != 0:
      for word_POS in findallpg:
        # get POS
        if word_POS.find('.//z_p_in_p-g') == None:
          continue

        POS = word_POS.find('.//z_p_in_p-g').text;

        if POS.strip() == 'verb':
          meanings = word_POS.findall('.//n-g');

          oxfordNouns[runhd] = OrderedDict();

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            meanings = word_POS.findall('.//d');
            if len(meanings)!= 0:
              readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
    else:
      POS = word.find('.//z_p');
      if POS != None:
        if POS.text.strip() == 'verb':

          oxfordNouns[runhd] = OrderedDict();
          meanings = word.findall('.//sd-g') or word.findall('.//n-g');

          if len(meanings) != 0:
            for iMeaning in range(len(meanings)):
              readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
          else:
            readContentOfWord(oxfordNouns,runhd,0,word,0);

    for word_2 in word.findall('.//entry'):

      # get word
      runhd = word_2.find('.//runhd');
      if runhd == None:
        continue

      runhd = runhd.text;

      if runhd == 'ballpark':
        adsf = 1;

      # get noun, verb of word
      findallpg = word_2.findall('.//p-g');
      if len(findallpg) != 0:
        for word_POS in findallpg:
          # get POS
          if word_POS.find('.//z_p_in_p-g') == None:
            continue

          POS = word_POS.find('.//z_p_in_p-g').text;

          if POS.strip() == 'verb':
            meanings = word_POS.findall('.//n-g');

            oxfordNouns[runhd] = OrderedDict();

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              meanings = word_POS.findall('.//d');
              if len(meanings)!= 0:
                readContentOfWord(oxfordNouns,runhd,0,word_POS,0);
      else:
        POS = word_2.find('.//z_p');
        if POS != None:
          if POS.text.strip() == 'verb':

            oxfordNouns[runhd] = OrderedDict();
            meanings = word_2.findall('.//sd-g') or word_2.findall('.//n-g');

            if len(meanings) != 0:
              for iMeaning in range(len(meanings)):
                readContentOfWord(oxfordNouns,runhd,iMeaning,meanings,1)
            else:
              readContentOfWord(oxfordNouns,runhd,0,word_2,0);

  ########################################
  return oxfordNouns;
  ########################################

####################################################################################################
#
# @brief:   write dictionary read from oxford to file
#
def writeDictFromOxfordToFile(filename, dict):

  file = open(filename, 'w');
  writer = csv.writer(file);

  for word in dict:
    # writer.writerow([word.encode('utf8')]);

    if dict[word] == None:
      continue

    for meaning in dict[word]:
      for key in dict[word][meaning]:
        if dict[word][meaning][key] == None:
          dict[word][meaning][key] = 'nn';
        writer.writerow([word.encode('utf8'),meaning,key,dict[word][meaning][key].encode('utf8')]);

  file.close();
  ########################################


__dict_nouns__ = readOxfordNouns()


def get_dict_nouns():
  return __dict_nouns__


def get_definitions_of_word(word):
  definitions = []
  if __dict_nouns__.has_key(word):
    dict_means_noun = __dict_nouns__[word]
    for index in range(len(dict_means_noun)):
      dict_noun = dict_means_noun[str(index)]
      definition = ""

#      if dict_noun.has_key('sd') and dict_noun['sd'] != None:
#        definition += dict_noun['sd']

      if dict_noun.has_key('d') and dict_noun['d'] != None:
        definition += ". " + dict_noun['d']

#      if dict_noun.has_key('xh') and dict_noun['xh'] != None:
#        definition += ". " + dict_noun['xh']

      definitions.append(definition)

  return definitions


# writeDictFromOxfordToFile("OxfordDict/b-detail_fixed.csv",__dict_nouns__);
