import os
from sklearn import svm
from scipy.stats.stats import pearsonr

path = "svm"
file_train = path + "/train/input_feature_values"
file_gold_train = path + "/train/gs_sen"
file_test = path + "/test/input_feature_values"
file_rs = path + "/test/result"

#file_gold_test = path + "/test/2012/demo/STS.golds.demo.txt"
#file_pearson = path + "/test/2012/demo/result_pearson.txt"


def run_svm():
  X = []
  y = []
  # Read file train
  for line in open(file_train):
    features = line.split("\t")
    F = []
    for f in features:
      F.append(float(f))
    X.append(F)
  # Read file gold of train
  for line in open(file_gold_train):
    y.append(float(line))

  # Read file test
  T = []
  for line in open(file_test):
    features = line.split("\t")
    F = []
    for f in features:
      F.append(float(f))
    T.append(F)
  # Init SVR
  clf = svm.SVR()
  print(clf.fit(X, y))
  # Run SVR
  rs = clf.predict(T)
  # print(rs)

  # Write result
  f = open(file_rs, 'w')
  for r in rs:
    f.write(str(r) + "\n")
  f.close()

  ## Read file gold of test
  #g = []
  #for line in open(file_gold_test):
  #    g.append(float(line))
  ## Compute Pearson
  #p = pearsonr(rs, g)
  #print("pearson correlation coefficient = " + str(p[0]))
  #
  #
  #f = open(file_pearson, 'w')
  #f.write("Pearson correlation coefficient = " + str(p[0]))
  #f.close()
  #
  #print("FINISH!")
