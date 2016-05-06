import svm.InputSVM as svmData
import svm.main_svm as svm
import svm.SimViaSVM as sim
import svm.ReadSVMResult as readSVMResult
import Util

#Util.remove_files_in_path("svm/train/")
Util.remove_files_in_path("svm/test/")
#
#print "train ..."
svmData.create_input_for_train_svm_via_vn()
#
print "run svm..."
svmData.create_input_for_test_svm()
svm.run_svm()
#
print "turning ..."
readSVMResult.read_svm_result()
sim.train_sim_definition()
##


#import svm.LSA as lsa
#Util.remove_files_in_path("svm/dataWn/")
#lsa.get_wn_data()
#
import subprocess
subprocess.call(['speech-dispatcher'])        #start speech dispatcher
subprocess.call(['spd-say', '"I am happy"'])
