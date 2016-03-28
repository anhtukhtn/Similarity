import SimilarityDefinition.SimOxWnDefinition as Sim
import svm.GoldDataSVM as svmData
import svm.main_svm as svm
import svm.SimViaSVM as sim
import svm.ReadSVMResult as readSVMResult
import Util

Util.remove_files_in_path("svm/train/")
print "train"
Util.remove_files_in_path("svm/test/")
print "test"

svmData.create_input_for_train()
svmData.cal_features_for_train()

#
svmData.create_input_for_test()
svmData.cal_features_for_test()
svm.run_svm()
readSVMResult.read_svm_result()
sim.train_sim_definition()

#Sim.train_sim_definition()

import subprocess
subprocess.call(['speech-dispatcher'])        #start speech dispatcher
subprocess.call(['spd-say', '"go go go"'])
