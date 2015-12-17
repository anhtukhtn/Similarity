__author__ = 'tu'

import CompareVietNetOxford

goldData = CompareVietNetOxford.readResultFile("Results/parameters/VN_Ox/"+"compare_VN_Ox.csv");

def compareGoldWithResult(dictResult,WORD):
  tp = 0.;
  tn = 0.;
  fn = 0.;
  fp = 0.;

  print dictResult
  print goldData[WORD]

  for row in range(len(dictResult)):
    for col in range(len(dictResult[row])):
      result = dictResult[row][col]
      gold = goldData[WORD][row][col]

      if result != 1:
        result = 0;

      if result == gold and gold == 1:
        tp += 1.;
      elif result == gold and gold == 0:
        tn += 1.;
      elif result != gold and gold == 1:
        fn += 1.;
      elif result != gold and gold == 0:
        fp += 1.;

  precision = tp / (tp + fp);
  recall = tp / (tp + fn);
  accuracy = (tp + tn) / (tp + tn + fp + fn);

  return (precision, recall, accuracy)
  ########################################

