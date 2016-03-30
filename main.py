import SimilarityDefinition.SimOxWnDefinition as Sim
import svm.InputSVM as svmData
import svm.GoldDataSVM as svmGoldData
import svm.main_svm as svm
import svm.SimViaSVM as sim
import svm.ReadSVMResult as readSVMResult
import Util

Util.remove_files_in_path("svm/train/")
Util.remove_files_in_path("svm/test/")

#svmGoldData.create_input_for_train()
#svmGoldData.cal_features_for_train()

print "train ..."
svmData.create_input_for_train_svm()

print "run svm..."
svmData.create_input_for_test_svm()
svm.run_svm()

print "turning ..."
readSVMResult.read_svm_result()
sim.train_sim_definition()

import subprocess
subprocess.call(['speech-dispatcher'])        #start speech dispatcher
subprocess.call(['spd-say', '"go go go"'])
