__author__ = 'tu'

#!/usr/bin/env python
# -*- coding: utf-8 -

import csv
import time

####################################################################################################
#
# @brief:  write matrix 2d to csv file
#
# @param: filename
#
# @param: row
#         first row
#
# @param: matrix_2d
#         arr 2d data
#
def write_to_excel_file(filename, row, matrix_2d):

  file = open(filename, 'w');
  writer = csv.writer(file);
  writer.writerow(row);
  for values in matrix_2d:
    writer.writerow(values);

  file.close();
  ########################################

def append_to_excel_file(filename, row, matrix_2d):

  file = open(filename, 'a');
  writer = csv.writer(file);
  writer.writerow(row);
  for values in matrix_2d:
    writer.writerow(values);

  writer.writerow([]);
  file.close();
  ########################################

def append_result_to_excel_file(filename, values):

  try:
    file = open(filename, 'a');
  except IOError:
    time.sleep(1)
    append_result_to_excel_file(filename,values)
  with file:
    writer = csv.writer(file);
    writer.writerow(values);
    file.close();
  ########################################

# a = [[1,2,3],[4,5,6],[7,8,9]]
# write_to_excel_file("temp.csv",a,a)