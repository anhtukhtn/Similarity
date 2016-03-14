import SimilarityDefinition.SimOxWnDefinition as Sim

Sim.train_sim_definition()

import subprocess
subprocess.call(['speech-dispatcher'])        #start speech dispatcher
subprocess.call(['spd-say', '"go go go"'])
