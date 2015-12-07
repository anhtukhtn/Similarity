__author__ = 'tu'

#!/usr/bin/env python
# -*- coding: utf-8 -


def readVietNetFile():

  dictVietNet = {};
  print dictVietNet

  f = open("WN/VietNet - A_B.csv",'r');
  print  f.readline();
  index = 0;

  line = f.readline();
  while (line):

    # print line

    phrases = line.split("\t");

    if len(phrases) < 5:
      line = f.readline();
      continue

    if phrases[2] != "N":
      line = f.readline();
      continue


    arr_d_xh = phrases[4].split(";");

    if not dictVietNet.has_key(phrases[1]):
      dictVietNet[phrases[1]] = {};

    curIndex = len(dictVietNet[phrases[1]]);
    dictVietNet[phrases[1]][curIndex] = {};
    dictVietNet[phrases[1]][curIndex]["tv"] = phrases[3];
    # print dictVietNet[phrases[1]][curIndex]["tv"];
    dictVietNet[phrases[1]][curIndex]["d"] = arr_d_xh[0];

    # print dictVietNet[phrases[1]][curIndex]

    index += 1;

    line = f.readline();

  # print dictVietNet

  return dictVietNet
  ########################################


readVietNetFile()