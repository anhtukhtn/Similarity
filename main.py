import SimilarityDefinition.SimOxWnDefinition as Sim
import svm.GoldDataSVM as svmData
import svm.ParseOxWnSVM as parseOx
import svm.main_svm as svm
import svm.SimViaSVM as sim
import svm.ReadSVMResult as readSVMResult


svmData.create_input_for_train()
svmData.cal_features_for_train()

#
parseOx.create_input_sens_for_test_svm()
svmData.cal_features_for_test()
svm.run_svm()
readSVMResult.read_svm_result()
sim.train_sim_definition()

#Sim.train_sim_definition()

#import subprocess
#subprocess.call(['speech-dispatcher'])        #start speech dispatcher
#subprocess.call(['spd-say', '"go go go"'])
