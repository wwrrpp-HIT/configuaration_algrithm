import time
import sys
sys.path.append('./configuration_algorithm')
from remoteApi import sim as vrep  # 导入库文件


class Coppeliasim:
    def __init__(self):
        pass

    def connect(self):
        """ Connect to the simulator"""
        print('Program started')
        vrep.simxFinish(-1)  # just in case, close all opened connections
        while True:
            self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to CoppeliaSim
            if self.clientID > -1:
                break
            else:
                time.sleep(0.2)
                print("Please run the simulation on vrep...")
        print("Connected to Vrep successfully!")
