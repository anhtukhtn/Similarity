__author__ = 'tu'

import CompareVietNetOxford

goldData = CompareVietNetOxford.readResultFile("Results/parameters/VN_Ox/"+"compare_VN_Ox_2.1.csv");
# print goldData
def compareGoldWithResult(dictResult,WORD):
  tp = 0.;
  tn = 0.;
  fn = 0.0;
  fp = 0.0;

  if not goldData.has_key(WORD):
    return (-1,0,0)

  # print dictResult
  # print goldData[WORD]

  for row in range(len(dictResult)):
    for col in range(len(dictResult[row])):
      result = dictResult[row][col]
      gold = goldData[WORD][row][col]

      gold = int(gold)
      if result != 1:
        result = 0;

      # print "pair result"
      # print result
      # print gold

      if (result == gold and gold == 1):
        tp += 1.;
        # print "tp"
      elif (result == gold and gold == 0):
        tn += 1.;
        # print "tn"
      elif (result != gold and gold == 1):
        fn += 1.;
        # print "fp"
      elif (result != gold and gold == 0):
        fp += 1.;
        # print "fp"

  # if tp == tn and tp == 0:
  #   print "tp tn == 0"
  #   print tp
  #   print tn
  #   print fp
  #   print fn

  precision = tp / (tp + fp + 0.000000001);
  recall = tp / (tp + fn + 0.000000001);
  accuracy = (tp + tn) / (tp + tn + fp + fn + 0.000000001);

  if precision == recall and precision == 0 and fn == fp and fn < 1:
    precision = -1;

  return (precision, recall, accuracy)
  ########################################


def compareGoldWithResult_without_cal_result(dictResult,WORD):
  tp = -1;
  tn = 0.;
  fn = 0.0;
  fp = 0.0;

  if not goldData.has_key(WORD):
    return (tp, tn, fn, fp)
  tp = 0.0

  for row in range(len(dictResult)):
    for col in range(len(dictResult[row])):
      result = dictResult[row][col]
      gold = goldData[WORD][row][col]

      gold = int(gold)
      if result != 1:
        result = 0;

      # print "pair result"
      # print result
      # print gold

      if (result == gold and gold == 1):
        tp += 1.;
        # print "tp"
      elif (result == gold and gold == 0):
        tn += 1.;
        # print "tn"
      elif (result != gold and gold == 1):
        fn += 1.;
        # print "fp"
      elif (result != gold and gold == 0):
        fp += 1.;
        # print "fp"

  return (tp, tn, fn, fp)
  ########################################

