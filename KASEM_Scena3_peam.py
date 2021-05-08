#!/usr/bin/env python
# coding: utf-8

# In[1]:


junction_id = {'KLONGTEI': 'cluster_1892287670_272491964_272492178',
      'RAMA4': 'cluster_272488163_282390730_66263210_66263222',
      'NARANONG': 'cluster_272488164_272492179_3457051443_61907354',
      'SUNLAKAKHON': 'gneJ83',
      'KASEMRAT': 'cluster_272448137_272555800_272555808_7660045934_7710268409',
      'ATTHAKAWI_RAMA4' : '270329335'}
junction_name = list(junction_id.keys())


# In[2]:


import gym
# import lxml.etree as ET
import csv
import json
import os, sys
os.environ['SUMO_HOME']='/usr/share/sumo'
tools = os.path.join(os.environ['SUMO_HOME'],'tools')
sys.path.append(tools)
import traci
import traci.constants as tc
import numpy as np
from sumolib import checkBinary
import datetime
import matplotlib
import matplotlib.pyplot as plt
import torch
import copy
import random
import pandas as pd
from multiprocessing.pool import ThreadPool
from itertools import zip_longest


# In[3]:


# send from peam
OPTION = {"lr":5e-4,"gamma":0.9,"beta": 0,"alpha":1}
data_json = json.dumps(OPTION)
print(type(data_json))
test_id = "_".join([str(e)+""+str(OPTION[e]) for e in OPTION.keys()])
test_id


# In[4]:


JAM_detector = ['SUNLAKAKHON_SB_FPX_TP1', 'RAMA4_SB_FP4_TP5', 'RAMA4_NB_FPX_TP5', 'NARANONG_SW_FPX_TP1', 'KASEMRAT_EB_FPX_TP2', 'SUNLAKAKHON_EB_FP3_TP4', 'MASUKGRIDLOCK_SUKHUMVUT_FPX_TP2', 'KASEMRAT_NB_FPX_TP3', 'RAMA4_EB_FPX_TP1', 'NARANONG_WB_FPX_TP2', 'MASUKGRIDLOCK_ARI_NB_FPX_TP2', 'KASEMRAT_EB_FPX_TP2_RAMA4', 'SUNLAKAKHON_WB_FP3_TP4', 'NARANONG_EB_FP1_TP2']
OCC_detector = ['RAMA4_NB_FP5_TP1', 'NARANONG_WB_FP4_TP5', 'RAMA4_WB_FP3_TP2', 'NARANONG_SB_FP1_TP2', 'NARANONG_NB_FP6_TP1', 'NARANONG_SB_FP5_TP6', 'RAMA4_EB_FP3_TP2']
FLOW_detector = ['NARANONG_WB_FP2_TP3_FLOW', 'SUNLAKAKHON_NB_FP2_TP3', 'SUNLAKAKHON_SB_FP1_TPX', 'SUNLAKAKHON_EB_FP4_TP1', 'RAMA4_WB_FP2_TP4', 'KLONGTEI_NB_FP3_TPX', 'KASEMRAT_EB_FP2_TP1', 'RAMA4_EB_FP1_TP3', 'NARANONG_EB_FP3_TP4']


# In[5]:


def send_to_peam1(output,test_id):
#     #do something??
    
#     server_ip = "https://exec.iotcloudserve.net/json-save/"

#     event_data = output

#     response = requests.post(server_ip+str(test_id), json=event_data)
#     #json_data = json.loads(response.text)
#     #print(type(response))
#     #print(response)

    return #response


# In[6]:


def send_to_peam2(trial):
    with open('"/Raytest/ray_results/my_exp4'+trial+"/result.json", 'r') as j:
        mean_reward_data = json.load(j)
    
    
#     server_ip = "https://exec.iotcloudserve.net/json-save/"

#     event_data = output

#     response = requests.post(server_ip+str(test_id), json=event_data)
#     #json_data = json.loads(response.text)
#     #print(type(response))
#     #print(response)

    return mean_reward_data 


# In[7]:


#reset the environment
def start(dateTimeObj):
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "KASEMRAT-SUMO-UsingBookNetFile/osm.sumocfg",
#                              "--summary-output", "summary/summary3"+dateTimeObj+".xml", 
                 '--start','true','--quit-on-end','true','--time-to-teleport','-1',
                '--lanechange.duration', '0.1'])


# In[8]:


# namelane_csv = pd.read_csv('namelane_KASEMRAT_nodot.csv')
# namelane_df = pd.DataFrame(namelane_csv, columns = ['name' , 'id']).dropna()
# NAME = namelane_df.set_index('name')
# ID = namelane_df.set_index('id')
# if NAME.loc['KASEMRAT_EB_0_0_XSXX','id'] == '459551209#3_0':
#     print('ok')


# In[9]:


namelane_csv = pd.read_csv('namelane_KASEMRAT_nodot.csv')
namelane_df = pd.DataFrame(namelane_csv, columns = ['name' , 'id']).dropna()
NAME = namelane_df.set_index('name')
ID = namelane_df.set_index('id')
detector_police = []
BACKLOG = {}
for name in ID.loc[:,'name']:
    n = name.split("_")
    if n[0]+"_"+n[1] not in BACKLOG.keys():
        BACKLOG[n[0]+"_"+n[1]] = [name]
    else:
        BACKLOG[n[0]+"_"+n[1]].append(name)


# In[10]:


def get_flow_sum(detector_id):
#     Speed (metres per sec) = flow (vehicle per sec) / density (veh per metre), Ajarn chaodit
#         flow= int(densityPerLane) * float(meanSpeed)#flow per lane
#     print('LastStepVehicleNumber', sum([traci.lanearea.getLastStepVehicleNumber(e) for e in detector_id]))
#     print('length', sum([traci.lanearea.getLength(i) for i in detector_id]))
#     density = sum([traci.lanearea.getLastStepVehicleNumber(e) for e in detector_id])/\
#     sum([traci.lanearea.getLength(i) for i in detector_id])
#     print('density', density)
    
    flow = sum(([traci.lanearea.getLastStepVehicleNumber(e)*traci.lanearea.getLastStepMeanSpeed(e)/traci.lanearea.getLength(e) for e in detector_id if
              traci.lanearea.getLastStepMeanSpeed(e) >= 0]))
    return flow


# In[11]:


def get_unjamlength_meters(detector_id): 
    detector_length = sum([traci.lanearea.getLength(e) for e in detector_id])
    unjamlength = detector_length - (sum([traci.lanearea.getJamLengthMeters(e) for e in detector_id])) #/detector_length
#     print("de", detector_length)
#     print(unjamlength)
    return unjamlength


# In[12]:


namedetector_csv = pd.read_csv('namedetector_KASEMRAT_flow.csv')
namedetector_df = pd.DataFrame(namedetector_csv, columns = ['name' , 'id'])
NAME_D = namedetector_df.set_index('name')
ID_D = namedetector_df.set_index('id')
listdetector = open("namedetector_KASEMRAT_flow.txt", "r")
detector = {}
for l in listdetector:
    l = l.strip().split(' ')
    if len(l)> 1:
        d = []
        for detec in l[2:]:
            if type(NAME_D.loc[detec,'id']) == str:
                d.append(NAME_D.loc[detec,'id'])
            else : d.append(NAME_D.loc[detec,'id'][0])
    if str(l[0])!= '':
        detector[str(l[0])] = d
list_detector= list(detector.keys())


# In[13]:


len(detector)


# In[14]:


BACKLOG


# In[15]:


def get_hot_encoding_current_phase():
    number_phase = [4,9,7,5,4,3]
    current_phase = [traci.trafficlight.getPhase(junction_id[key]) for key in junction_id.keys()]
#     current_phase = [0,2,1,1,1,1]
    hot_encoding_current_phase = np.array([])
    for i in range(len(current_phase)):
        binary_phase = np.zeros(number_phase[i])
        binary_phase[current_phase[i]] = 1
        hot_encoding_current_phase = np.concatenate((hot_encoding_current_phase, binary_phase), axis=None)
    return current_phase, hot_encoding_current_phase


# In[16]:


# RAMA4
RAMA4_EB_R = [NAME.loc['RAMA4_EB_1_4_XSXX','id'], NAME.loc['RAMA4_EB_0_3_XSRT','id']]
RAMA4_EB = [NAME.loc['KLONGTEI_EB_0_0_XSXX','id'],NAME.loc['KLONGTEI_EB_0_1_XSXX','id'],NAME.loc['KLONGTEI_EB_0_2_XSXX','id'],NAME.loc['KLONGTEI_EB_0_3_XSXX','id'],NAME.loc['KLONGTEI_EB_0_4_XSRT','id'],NAME.loc['KLONGTEI_EB_1_0_XSXX','id'],NAME.loc['KLONGTEI_EB_1_1_XSXX','id'],NAME.loc['KLONGTEI_EB_1_2_XSXX','id'],NAME.loc['KLONGTEI_EB_1_3_XSXX','id'],NAME.loc['KLONGTEI_EB_2_0_LSXX','id'],NAME.loc['KLONGTEI_EB_2_1_XSXX','id'],NAME.loc['KLONGTEI_EB_2_2_XSXX','id'],NAME.loc['KLONGTEI_EB_2_3_XSXX','id'],NAME.loc['KLONGTEI_EB_3_0_LSXX','id'],NAME.loc['KLONGTEI_EB_3_1_XSXX','id'],NAME.loc['KLONGTEI_EB_4_0_XSXX','id'],NAME.loc['KLONGTEI_EB_4_1_XSXX','id'],NAME.loc['KLONGTEI_EB_4_2_XSXX','id'],NAME.loc['KLONGTEI_EB_4_3_XSXX','id'],NAME.loc['KLONGTEI_EB_4_4_XSXX','id'],NAME.loc['KLONGTEI_EB_5_0_XSXX','id'],NAME.loc['KLONGTEI_EB_5_1_XSXX','id'],NAME.loc['KLONGTEI_EB_5_2_XSXX','id'],NAME.loc['KLONGTEI_EB_5_3_XSXX','id'],NAME.loc['RAMA4_EB_0_0_XSXX','id'],NAME.loc['RAMA4_EB_0_1_XSXX','id'],NAME.loc['RAMA4_EB_0_2_XSXX','id'],NAME.loc['RAMA4_EB_0_3_XSRT','id'],NAME.loc['RAMA4_EB_1_0_LSXX','id'],NAME.loc['RAMA4_EB_1_1_XSXX','id'],NAME.loc['RAMA4_EB_1_2_XSXX','id'],NAME.loc['RAMA4_EB_1_3_XSXX','id'],NAME.loc['RAMA4_EB_1_4_XSXX','id']]
RAMA4_SB = [NAME.loc['RAMA4_SB_0_0_XSXX','id'],NAME.loc['RAMA4_SB_0_1_XSXX','id'],NAME.loc['RAMA4_SB_0_2_XSRT','id'],NAME.loc['RAMA4_SB_1_0_LSXX','id'],NAME.loc['RAMA4_SB_1_1_XSXX','id'],NAME.loc['RAMA4_SB_1_2_XSXX','id'],NAME.loc['RAMA4_SB_1_3_XSXX','id'],NAME.loc['RAMA4_SB_2_0_XSXX','id'],NAME.loc['RAMA4_SB_2_1_XSXX','id'],NAME.loc['RAMA4_SB_2_2_XSXX','id'],NAME.loc['RAMA4_SB_3_0_XSXX','id'],NAME.loc['RAMA4_SB_3_1_XSXX','id'],NAME.loc['RAMA4_SB_3_2_XSXX','id'],NAME.loc['RAMA4_SB_3_3_XSRX','id'],NAME.loc['RAMA4_SB_4_0_XSXX','id'],NAME.loc['RAMA4_SB_4_1_XSXX','id'],NAME.loc['RAMA4_SB_4_2_XSXX','id'],NAME.loc['RAMA4_SB_5_0_XSXX','id'],NAME.loc['RAMA4_SB_5_1_XSXX','id'],NAME.loc['RAMA4_SB_5_2_XSXX','id'],NAME.loc['RAMA4_SB_5_3_XSXX','id'],NAME.loc['RAMA4_SB_5_4_XSXX','id']]
RAMA4_NB = [NAME.loc['RAMA4_NB_0_0_XSXX','id'],NAME.loc['RAMA4_NB_0_1_XSXX','id'],NAME.loc['RAMA4_NB_0_2_XSRT','id'],NAME.loc['RAMA4_NB_1_0_LSXX','id'],NAME.loc['RAMA4_NB_1_1_XSXX','id'],NAME.loc['RAMA4_NB_1_2_XSXX','id'],NAME.loc['RAMA4_NB_1_3_XSXX','id'],NAME.loc['RAMA4_NB_2_0_XSXX','id'],NAME.loc['RAMA4_NB_2_1_XSXX','id'],NAME.loc['RAMA4_NB_2_2_XSXX','id'],NAME.loc['RAMA4_NB_3_0_XSXX','id'],NAME.loc['RAMA4_NB_3_1_XSXX','id']]
RAMA4_WB = [NAME.loc['RAMA4_WB_0_0_XSXX','id'],NAME.loc['RAMA4_WB_0_1_XSXX','id'],NAME.loc['RAMA4_WB_0_2_XSXX','id'],NAME.loc['RAMA4_WB_0_3_XSXX','id'],NAME.loc['RAMA4_WB_0_4_XSRT','id'],NAME.loc['RAMA4_WB_1_0_LSXX','id'],NAME.loc['RAMA4_WB_1_1_XSXX','id'],NAME.loc['RAMA4_WB_1_2_XSXX','id'],NAME.loc['RAMA4_WB_1_3_XSXX','id'],NAME.loc['RAMA4_WB_1_4_XSXX','id'],NAME.loc['RAMA4_WB_1_5_XSXX','id'],NAME.loc['RAMA4_WB_2_0_XSXX','id'],NAME.loc['RAMA4_WB_2_1_XSXX','id'],NAME.loc['RAMA4_WB_2_2_XSXX','id'],NAME.loc['RAMA4_WB_2_3_XSXX','id'],NAME.loc['RAMA4_WB_3_0_XSXX','id'],NAME.loc['RAMA4_WB_3_1_XSXX','id'],NAME.loc['RAMA4_WB_3_2_XSXX','id'],NAME.loc['RAMA4_WB_4_0_XSXX','id'],NAME.loc['RAMA4_WB_4_1_XSXX','id'],NAME.loc['RAMA4_WB_5_0_LSXX','id'],NAME.loc['RAMA4_WB_5_1_XSXX','id'],NAME.loc['RAMA4_WB_5_2_XSXX','id'],NAME.loc['RAMA4_WB_6_0_LSXX','id'],NAME.loc['RAMA4_WB_6_1_XSXX','id'],NAME.loc['RAMA4_WB_6_2_XSXX','id']]
RAMA4_WB_R = [NAME.loc['RAMA4_WB_0_4_XSRT','id'], NAME.loc['RAMA4_WB_1_5_XSXX','id'],NAME.loc['RAMA4_WB_2_3_XSXX','id']]
KLONGTEI_NB = [NAME.loc['KLONGTEI_NB_0_0_LSXX','id'],NAME.loc['KLONGTEI_NB_0_1_XSXX','id'],NAME.loc['KLONGTEI_NB_0_2_XSXX','id'],NAME.loc['KLONGTEI_NB_0_3_XSRT','id'],NAME.loc['KLONGTEI_NB_1_0_LSXX','id'],NAME.loc['KLONGTEI_NB_1_1_XSXX','id'],NAME.loc['KLONGTEI_NB_1_2_XSXX','id'],NAME.loc['KLONGTEI_NB_1_3_XSXX','id'],NAME.loc['KLONGTEI_NB_2_0_LSXX','id'],NAME.loc['KLONGTEI_NB_2_1_XSXX','id'],NAME.loc['KLONGTEI_NB_2_2_XSXX','id'],NAME.loc['KLONGTEI_NB_2_3_XSXX','id']]
# NARANONG
NARANONG_EB = [NAME.loc['NARANONG_EB_0_0_LSXX','id'],NAME.loc['NARANONG_EB_0_1_XSRT','id'],NAME.loc['NARANONG_EB_1_0_XSXX','id'],NAME.loc['NARANONG_EB_1_1_XSXX','id'],NAME.loc['NARANONG_EB_2_0_XSXX','id'],NAME.loc['NARANONG_EB_2_1_XSXX','id'],NAME.loc['NARANONG_EB_2_2_XSXX','id'],NAME.loc['NARANONG_EB_3_0_XSXX','id'],NAME.loc['NARANONG_EB_3_1_XSRX','id'],NAME.loc['NARANONG_EB_4_0_LSXX','id'],NAME.loc['NARANONG_EB_4_1_XSXX','id'],NAME.loc['NARANONG_EB_5_0_LSXX','id'],NAME.loc['NARANONG_EB_5_1_XSRX','id']]
NARANONG_WB = [NAME.loc['NARANONG_WB_0_0_LSXX','id'],NAME.loc['NARANONG_WB_0_1_XSXX','id'],NAME.loc['NARANONG_WB_0_2_XSXX','id'],NAME.loc['NARANONG_WB_0_3_XSRT','id'],NAME.loc['NARANONG_WB_1_0_XSXX','id'],NAME.loc['NARANONG_WB_1_1_XSXX','id'],NAME.loc['NARANONG_WB_1_2_XSXX','id'],NAME.loc['NARANONG_WB_2_0_LSXX','id'],NAME.loc['NARANONG_WB_2_1_XSXX','id'],NAME.loc['NARANONG_WB_2_2_XSXX','id'],NAME.loc['NARANONG_WB_3_0_XSXX','id'],NAME.loc['NARANONG_WB_3_1_XSXX','id'],NAME.loc['NARANONG_WB_3_2_XSXX','id'],NAME.loc['NARANONG_WB_3_3_XSXX','id'],NAME.loc['NARANONG_WB_4_0_XSXX','id'],NAME.loc['NARANONG_WB_4_1_XSXX','id'],NAME.loc['NARANONG_WB_4_2_XSXX','id']]
NARANONG_SB = [NAME.loc['NARANONG_SB_0_0_LSXX','id'],NAME.loc['NARANONG_SB_0_1_XSXX','id'],NAME.loc['NARANONG_SB_0_2_XSRX','id'],NAME.loc['NARANONG_SB_1_0_LSXX','id'],NAME.loc['NARANONG_SB_1_1_XSXX','id'],NAME.loc['NARANONG_SB_1_2_XSXX','id'],NAME.loc['NARANONG_SB_1_3_XSXX','id'],NAME.loc['NARANONG_SB_2_0_XSXX','id'],NAME.loc['NARANONG_SB_2_1_XSXX','id'],NAME.loc['NARANONG_SB_2_2_XSXX','id'],NAME.loc['NARANONG_SB_2_3_XSXX','id']]
NARANONG_SW = [NAME.loc['NARANONG_SW_0_1_XSRX','id'],NAME.loc['NARANONG_SW_1_0_XSXX','id'],NAME.loc['NARANONG_SW_1_1_XSXX','id'],NAME.loc['NARANONG_SW_1_2_XSXX','id'],NAME.loc['NARANONG_SW_1_3_XSXX','id'],NAME.loc['NARANONG_SW_2_0_XSXX','id'],NAME.loc['NARANONG_SW_2_1_XSXX','id'],NAME.loc['NARANONG_SW_2_2_XSXX','id']]
NARANONG_NB = [NAME.loc['NARANONG_NB_0_0_XSXX','id'],NAME.loc['NARANONG_NB_0_1_XSRX','id'],NAME.loc['NARANONG_NB_1_0_LSXX','id'],NAME.loc['NARANONG_NB_1_1_XSXX','id'],NAME.loc['NARANONG_NB_1_2_XSXX','id'],NAME.loc['NARANONG_NB_2_0_XSXX','id'],NAME.loc['NARANONG_NB_2_1_XSXX','id']]
NARANONG_EB_R = [NAME.loc['NARANONG_EB_0_1_XSRT','id']]
# SUNLAKAKHON
SUNLAKAKHON_EB = [NAME.loc['SUNLAKAKHON_EB_0_0_LSXX','id'],NAME.loc['SUNLAKAKHON_EB_0_1_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_0_2_XSRT','id'],NAME.loc['SUNLAKAKHON_EB_1_0_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_1_1_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_1_2_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_1_3_XSRX','id'],NAME.loc['SUNLAKAKHON_EB_2_0_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_2_1_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_2_2_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_3_0_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_3_1_XSXX','id'],NAME.loc['SUNLAKAKHON_EB_4_0_XSXX','id']]
SUNLAKAKHON_WB = [NAME.loc['SUNLAKAKHON_WB_0_0_LSXX','id'],NAME.loc['SUNLAKAKHON_WB_0_1_XSXX','id'],NAME.loc['SUNLAKAKHON_WB_0_2_XSRX','id'],NAME.loc['SUNLAKAKHON_WB_1_0_XSXX','id'],NAME.loc['SUNLAKAKHON_WB_1_1_XSXX','id'],NAME.loc['SUNLAKAKHON_WB_1_2_XSXX','id'],NAME.loc['SUNLAKAKHON_WB_2_0_XSXX','id'],NAME.loc['SUNLAKAKHON_WB_2_1_XSXX','id']]
SUNLAKAKHON_SB = [NAME.loc['SUNLAKAKHON_SB_0_0_LSXX','id'],NAME.loc['SUNLAKAKHON_SB_0_1_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_0_2_XSRT','id'],NAME.loc['SUNLAKAKHON_SB_1_0_LSXX','id'],NAME.loc['SUNLAKAKHON_SB_1_1_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_1_2_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_1_3_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_2_0_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_2_1_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_2_2_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_3_0_LSXX','id'],NAME.loc['SUNLAKAKHON_SB_3_1_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_3_2_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_3_3_XSRX','id'],NAME.loc['SUNLAKAKHON_SB_4_0_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_4_1_XSXX','id'],NAME.loc['SUNLAKAKHON_SB_4_2_XSXX','id']]
SUNLAKAKHON_NB = [NAME.loc['SUNLAKAKHON_NB_0_0_LSXX','id'],NAME.loc['SUNLAKAKHON_NB_0_1_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_0_2_XSRX','id'],NAME.loc['SUNLAKAKHON_NB_1_0_LSXX','id'],NAME.loc['SUNLAKAKHON_NB_1_1_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_1_2_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_2_0_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_2_1_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_2_2_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_3_0_LSXX','id'],NAME.loc['SUNLAKAKHON_NB_3_1_XSXX','id'],NAME.loc['SUNLAKAKHON_NB_3_2_XSXX','id']]

# KASEMRAT
KASEMRAT_EB = [NAME.loc['KASEMRAT_EB_0_0_XSXX','id'],NAME.loc['KASEMRAT_EB_0_1_XSXX','id'],NAME.loc['KASEMRAT_EB_0_2_XSXX','id'],NAME.loc['KASEMRAT_EB_0_3_XSRT','id'],NAME.loc['KASEMRAT_EB_1_0_LSXX','id'],NAME.loc['KASEMRAT_EB_1_1_XSXX','id'],NAME.loc['KASEMRAT_EB_1_2_XSXX','id'],NAME.loc['KASEMRAT_EB_1_3_XSXX','id'],NAME.loc['KASEMRAT_EB_2_0_LSXX','id'],NAME.loc['KASEMRAT_EB_2_1_XSXX','id'],NAME.loc['KASEMRAT_EB_2_2_XSXX','id'],NAME.loc['KASEMRAT_EB_3_0_LSXX','id'],NAME.loc['KASEMRAT_EB_3_1_XSXX','id'],NAME.loc['KASEMRAT_EB_3_2_XSXX','id'],NAME.loc['KASEMRAT_EB_4_0_LSXX','id'],NAME.loc['KASEMRAT_EB_4_1_XSXX','id'],NAME.loc['KASEMRAT_EB_4_2_XSXX','id'],NAME.loc['KASEMRAT_EB_5_0_LSXX','id'],NAME.loc['KASEMRAT_EB_5_1_XSXX','id'],NAME.loc['KASEMRAT_EB_5_2_XSXX','id'],NAME.loc['KASEMRAT_EB_5_3_XSXX','id'],NAME.loc['KASEMRAT_EB_6_0_LSXX','id'],NAME.loc['KASEMRAT_EB_6_1_XSXX','id'],NAME.loc['KASEMRAT_EB_6_2_XSXX','id'],NAME.loc['KASEMRAT_EB_6_3_XSXX','id'],NAME.loc['KASEMRAT_EB_7_0_LSXX','id'],NAME.loc['KASEMRAT_EB_7_1_XSXX','id'],NAME.loc['KASEMRAT_EB_7_2_XSXX','id'],NAME.loc['KASEMRAT_EB_7_3_XSXX','id'],NAME.loc['KASEMRAT_EB_8_0_XSXX','id'],NAME.loc['KASEMRAT_EB_8_1_XSXX','id'],NAME.loc['KASEMRAT_EB_8_2_XSXX','id'],NAME.loc['KASEMRAT_EB_8_3_XSXX','id'],NAME.loc['KASEMRAT_EB_8_4_XSXX','id'],NAME.loc['KASEMRAT_EB_9_0_XSXX','id'],NAME.loc['KASEMRAT_EB_9_1_XSXX','id'],NAME.loc['KASEMRAT_EB_9_2_XSXX','id'],NAME.loc['KASEMRAT_EB_9_3_XSXX','id']]
KASEMRAT_WB = [NAME.loc['KASEMRAT_WB_0_0_LSXX','id'],NAME.loc['KASEMRAT_WB_0_1_XSXX','id'],NAME.loc['KASEMRAT_WB_0_2_XSXX','id'],NAME.loc['KASEMRAT_WB_1_0_XSXX','id'],NAME.loc['KASEMRAT_WB_1_1_XSXX','id'],NAME.loc['KASEMRAT_WB_1_2_XSXX','id'],NAME.loc['KASEMRAT_WB_1_3_XSRX','id'],NAME.loc['KASEMRAT_WB_2_0_XSXX','id'],NAME.loc['KASEMRAT_WB_2_1_XSXX','id'],NAME.loc['KASEMRAT_WB_2_2_XSXX','id'],NAME.loc['KASEMRAT_WB_3_0_LSXX','id'],NAME.loc['KASEMRAT_WB_3_1_XSXX','id'],NAME.loc['KASEMRAT_WB_3_2_XSXX','id']]
KASEMRAT_NB = [NAME.loc['KASEMRAT_NB_0_0_LSXX','id'],NAME.loc['KASEMRAT_NB_0_1_XSXX','id'],NAME.loc['KASEMRAT_NB_0_2_XSRX','id'],NAME.loc['KASEMRAT_NB_1_0_LSXX','id'],NAME.loc['KASEMRAT_NB_1_1_XSXX','id'],NAME.loc['KASEMRAT_NB_1_2_XSXX','id'],NAME.loc['KASEMRAT_NB_2_0_XSXX','id'],NAME.loc['KASEMRAT_NB_2_1_XSXX','id'],NAME.loc['KASEMRAT_NB_3_0_LSXX','id'],NAME.loc['KASEMRAT_NB_3_1_XSXX','id'],NAME.loc['KASEMRAT_NB_3_2_XSXX','id'],NAME.loc['KASEMRAT_NB_3_3_XSRT','id'],NAME.loc['KASEMRAT_NB_4_0_XSXX','id'],NAME.loc['KASEMRAT_NB_4_1_XSXX','id'],NAME.loc['KASEMRAT_NB_4_2_XSXX','id'],NAME.loc['KASEMRAT_NB_5_0_XSXX','id'],NAME.loc['KASEMRAT_NB_5_1_XSXX','id'],NAME.loc['KASEMRAT_NB_5_2_XSXX','id'],NAME.loc['KASEMRAT_NB_5_3_XSXX','id'],NAME.loc['KASEMRAT_NB_6_0_XSXX','id'],NAME.loc['KASEMRAT_NB_6_1_XSXX','id'],NAME.loc['KASEMRAT_NB_6_2_XSXX','id']]
KASEMRAT_EB_R = [NAME.loc['KASEMRAT_EB_0_3_XSRT','id'],NAME.loc['KASEMRAT_EB_1_3_XSXX','id']]

MASUKGRIDLOCK = [NAME.loc['MASUKGRIDLOCK_ARI_NB_0_0_LSXX','id'],NAME.loc['MASUKGRIDLOCK_MASUK_WB_0_0_LSRX','id'],NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_0_0_XSRT','id'],NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_1_0_LSXT','id'],NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_2_0_LXXX','id']]
SUKHUMVIT = [NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_0_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_1_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_2_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_3_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_4_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_5_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_6_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_7_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_8_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_9_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT22_SB_10_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT24_SB_0_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT24_SB_1_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT24_SB_2_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT24_SB_3_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_0_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_1_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_2_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_3_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_4_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_5_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_6_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_7_0_XSXX','id'],NAME.loc['MASUKGRIDLOCK_SUKHUMVIT26_SB_8_0_XSXX','id']]
ROAD = [RAMA4_EB_R,RAMA4_EB,RAMA4_SB,RAMA4_NB,RAMA4_WB,RAMA4_WB_R,KLONGTEI_NB,NARANONG_EB,NARANONG_WB,NARANONG_SB,NARANONG_SW,
    NARANONG_NB,NARANONG_EB_R,SUNLAKAKHON_EB,SUNLAKAKHON_WB,SUNLAKAKHON_SB,SUNLAKAKHON_NB,KASEMRAT_EB,KASEMRAT_WB,KASEMRAT_NB,KASEMRAT_EB_R,MASUKGRIDLOCK]

def get_state_attention(current_phase, hot_encoding_current_phase):
    MAP_RAMA4 = ['RAMA4_EB_FPX_TP1', 'KASEMRAT_EB_FPX_TP2_RAMA4', 'NARANONG_SW_FPX_TP1', 'RAMA4_EB_FP1_TP3', 
                  'RAMA4_NB_FPX_TP5', 'RAMA4_WB_FP2_TP4', 'RAMA4_EB_FP3_TP2', 'RAMA4_WB_FP3_TP2', 'RAMA4_SB_FP4_TP5', 
                  'RAMA4_NB_FP5_TP1']
    MAP_KLONGTEI = ['NARANONG_SB_FP5_TP6', 'RAMA4_EB_FP3_TP2', 'RAMA4_EB_FP1_TP3', 'KLONGTEI_NB_FP3_TPX']
    MAP_NARANONG =  ['RAMA4_NB_FPX_TP5', 'NARANONG_SB_FP1_TP2', 'NARANONG_EB_FP1_TP2', 'NARANONG_WB_FPX_TP2', 
                    'NARANONG_WB_FP2_TP3_FLOW', 'NARANONG_SW_FPX_TP1', 'NARANONG_EB_FP3_TP4',
                     'NARANONG_WB_FP4_TP5', 'NARANONG_SB_FP5_TP6', 'NARANONG_NB_FP6_TP1', 'KLONGTEI_NB_FP3_TPX','SUNLAKAKHON_EB_FP3_TP4']
    MAP_SUNLAKAKHON = ['NARANONG_WB_FPX_TP2','SUNLAKAKHON_SB_FP1_TPX','SUNLAKAKHON_NB_FP2_TP3', 'SUNLAKAKHON_EB_FP3_TP4', 
                       'SUNLAKAKHON_WB_FP3_TP4', 'SUNLAKAKHON_EB_FP4_TP1', 'SUNLAKAKHON_SB_FPX_TP1','KASEMRAT_NB_FPX_TP3']
    MAP_KASEMRAT = ['SUNLAKAKHON_SB_FPX_TP1', 'MASUKGRIDLOCK_ARI_NB_FPX_TP2','KASEMRAT_EB_FP2_TP1',
                    'MASUKGRIDLOCK_SUKHUMVUT_FPX_TP2',
                    'KASEMRAT_NB_FPX_TP3',
                   'KASEMRAT_EB_FPX_TP2_RAMA4', 'KASEMRAT_EB_FPX_TP2'] 
    MAP_ATTHAKAWI_RAMA4 = ['SUNLAKAKHON_SB_FPX_TP1', 'MASUKGRIDLOCK_ARI_NB_FPX_TP2','MASUKGRIDLOCK_SUKHUMVUT_FPX_TP2',
                           'KASEMRAT_EB_FP2_TP1', 'KASEMRAT_NB_FPX_TP3','KASEMRAT_EB_FPX_TP2_RAMA4', 'KASEMRAT_EB_FPX_TP2'] 
                         
#     MAP_KLONGTEI = [RAMA4_EB_R,RAMA4_EB,KLONGTEI_NB]
#     MAP_NARANONG = [NARANONG_EB,NARANONG_WB,NARANONG_SB,NARANONG_SW,NARANONG_NB,NARANONG_EB_R, RAMA4_NB,KLONGTEI_NB]
#     MAP_SUNLAKAKHON = [SUNLAKAKHON_EB,SUNLAKAKHON_WB,SUNLAKAKHON_SB,SUNLAKAKHON_NB,NARANONG_WB]
#     MAP_KASEMRAT = [KASEMRAT_EB,KASEMRAT_WB,KASEMRAT_NB,KASEMRAT_EB_R,MASUKGRIDLOCK,SUNLAKAKHON_SB]
#     MAP_ATTHAKAWI_RAMA4 = [KASEMRAT_EB,KASEMRAT_WB,KASEMRAT_NB,KASEMRAT_EB_R,MASUKGRIDLOCK,SUNLAKAKHON_SB]
    
#     ROAD = [RAMA4_EB_R,RAMA4_EB,RAMA4_SB,RAMA4_NB,RAMA4_WB,RAMA4_WB_R,KLONGTEI_NB,NARANONG_EB,NARANONG_WB,NARANONG_SB,NARANONG_SW,
#     NARANONG_NB,NARANONG_EB_R,SUNLAKAKHON_EB,SUNLAKAKHON_WB,SUNLAKAKHON_SB,SUNLAKAKHON_NB,KASEMRAT_EB,KASEMRAT_WB,KASEMRAT_NB,KASEMRAT_EB_R,MASUKGRIDLOCK]
    
    MAP = [MAP_KLONGTEI, MAP_RAMA4, MAP_NARANONG, MAP_SUNLAKAKHON,  MAP_KASEMRAT, MAP_ATTHAKAWI_RAMA4]
    state = {}
#     hothot = {}
#     number_phase = [4,9,7,5,4,3]
#     begin_index = 0
#     hot_encode_real = list(np.zeros(32))
#     for i in range(len(hot_encoding_current_phase)):
#         if hot_encoding_current_phase[i] >= 0:
#             hot_encode_real[i] = 1
#     for i in range(len(number_phase)):
#         hot = hot_encoding_current_phase[begin_index:begin_index+number_phase[i]]
# #         print(hot_encode_real[:begin_index]+list(hot)+hot_encode_real[begin_index:])
#         hothot[i] = np.array(hot_encode_real[:begin_index]+list(hot)+hot_encode_real[begin_index+number_phase[i]:])
#         begin_index += number_phase[i]
    for i in range(len(current_phase)):
        state_attention = np.zeros(30)
        for e in MAP[i]:
#             state_attention = np.zeros(31)
            if e in OCC_detector :
                statei = get_occupancy_average_percent(detector[e])
            elif e in JAM_detector :
                statei = get_unjamlength_meters(detector[e])
            elif e in FLOW_detector:
                statei = get_flow_sum(detector[e])
            else: print(e)
            
            Index_detector = list_detector.index(e) 
            state_attention[Index_detector] = statei
        state[i] = np.concatenate((state_attention, hot_encoding_current_phase), axis=None).astype(np.float16)
#         print(state)
    return state


# In[17]:


def read_summary_xml(dateTimeObj):
    meanWaitingTime = []
    meanTravelTime = []
    meanSpeed = []
    tree = ET.parse('summary/summary3'+dateTimeObj+'.xml')
    summary = tree.getroot()
    for step in summary:
        list1 = step.attrib
        meanWaitingTime.append(float(list1["meanWaitingTime"]))
        meanTravelTime.append(float(list1["meanTravelTime"]))
        meanSpeed.append(float(list1["meanSpeed"]))
    meanWaitingTime_avg = sum(meanWaitingTime)/len(meanWaitingTime)
    meanTravelTime_avg = sum(meanTravelTime)/len(meanTravelTime)
    meanSpeed_avg = sum(meanSpeed)/len(meanSpeed)
    os.remove('summary/summary3'+dateTimeObj+'.xml')
    return meanWaitingTime_avg,meanTravelTime_avg,meanSpeed_avg


# In[18]:


def get_mean_speed():
    
    speed = [traci.lanearea.getLastStepMeanSpeed(e)*traci.lanearea.getLastStepVehicleNumber(e) for e in NAME.loc[:,'id'] if traci.lanearea.getLastStepMeanSpeed(e)>=0]
#     print(speed)
    num_veh = [traci.lanearea.getLastStepVehicleNumber(i) for i in NAME.loc[:,'id']]
    mean_speed = sum(speed)/max(sum(num_veh),1)
#     print('speed',mean_speed)
    return mean_speed


# In[19]:


def read_summary_xml(dateTimeObj):
    meanWaitingTime = []
    meanTravelTime = []
    meanSpeed = []
    tree = ET.parse('summary/summary3'+dateTimeObj+'.xml')
    summary = tree.getroot()
    for step in summary:
        list1 = step.attrib
        meanWaitingTime.append(float(list1["meanWaitingTime"]))
        meanTravelTime.append(float(list1["meanTravelTime"]))
        meanSpeed.append(float(list1["meanSpeed"]))
    meanWaitingTime_avg = sum(meanWaitingTime)/len(meanWaitingTime)
    meanTravelTime_avg = sum(meanTravelTime)/len(meanTravelTime)
    meanSpeed_avg = sum(meanSpeed)/len(meanSpeed)
    os.remove('summary/summary3'+dateTimeObj+'.xml')
    return meanWaitingTime_avg,meanTravelTime_avg,meanSpeed_avg


# In[20]:


def get_occupancy_average_percent(detector_id): 
    #get occupancy average for all detector in list of detector_id and scale by (Vehicle Length + MinimumGap)/MinimumGap 
    #Vehicle Length = 4.62 MinimumGap = 2.37
#     occupancy = (sum([traci.lanearea.getJamLengthMeters(e) for e in detector_id]))/\
#                  sum([traci.lanearea.getLength(e) for e in detector_id])
    
    occupancy = (sum([traci.lanearea.getLastStepOccupancy(e)*traci.lanearea.getLength(e) for e in detector_id]))/                 sum([traci.lanearea.getLength(e) for e in detector_id])*((4.62+2.37)/4.62)
#     print(occupancy)
    return occupancy


# In[21]:


KASEMRAT_loopcoil = ['L459551209#3_0', 'L459551209#3_1', 'L459551209#3_2', 'L459551209#3_3', 'L321845933#3_0', 'L321845933#3_1', 'L321845933#3_2', 'L820373194#0_0', 'L820373194#0_1', 'L820373194#0_2']
KLONGTEI_loopcoil = ['L825786400_0','L825786400_1', 'L825786400_2', 'L825786400_3', 'L825786400_4', 'L25047974#2_0', 'L25047974#2_1', 'L25047974#2_2', 'L25047974#2_3', 'L481971011#1_0', 'L481971011#1_1', 'L481971011#1_2', 'L481971011#1_3', 'L481971011#1_4']
NARANONG_loopcoil = ['L25053626_0','L25053626_1', 'L824116551#0_0', 'L824116551#0_1', 'L824116544_0', 'L824116544_1', 'L824116544_2', 'L824116550#0_0', 'L824116550#0_1', 'L338595767_0', 'L338595767_1', 'L338595767_2', 'L338595767_3']
SUNLAKAKHON_loopcoil = ['L824116555#3_0','L824116555#3_1', 'L824116555#3_2', 'L153225687#13_0', 'L153225687#13_1', 'L153225687#13_2', 'L321845932#1_0', 'L321845932#1_1', 'L321845932#1_2', 'L45033613#1_0', 'L45033613#1_1', 'L45033613#1_2']
RAMA4_loopcoil = ['L825786410_0','L825786410_1', 'L825786410_2', 'L825786410_3', 'L824116545_0', 'L824116545_1', 'L824116545_2', 'L821785867_0', 'L821785867_1', 'L821785867_2', 'L825786416_0', 'L825786416_1', 'L825786416_2', 'L825786416_3', 'L825786416_4']
ATTHAKAVI_RAMA4_loopcoil = ['L27702347#6_0', 'L27702347#6_1', 'L820340552#2_0', 'L820340552#2_1', 'L820340552#2_2']

ALL_loopcoil = KASEMRAT_loopcoil+KLONGTEI_loopcoil+NARANONG_loopcoil+SUNLAKAKHON_loopcoil+RAMA4_loopcoil+ATTHAKAVI_RAMA4_loopcoil


# In[22]:


def get_throughput(loopID):
#     loopID = traci.inductionloop.getIDList()
    throughput = sum([traci.inductionloop.getLastStepVehicleNumber(i) for i in loopID if traci.inductionloop.getLastStepMeanSpeed(i) > 0])  #if traci.inductionloop.getLastStepMeanSpeed(i) > 0
    return throughput


# In[23]:


def get_drawback(laneID):
#     laneID = traci.lane.getIDList()
    drawback = sum([traci.lanearea.getLastStepVehicleNumber(i) for i in laneID])
    return drawback


# In[24]:



GRIDLOCKAREA = RAMA4_NB+RAMA4_WB+KLONGTEI_NB+NARANONG_WB+NARANONG_SB+NARANONG_SW+SUNLAKAKHON_EB+SUNLAKAKHON_SB+KASEMRAT_EB+KASEMRAT_NB


# In[25]:


KASEMRAT_EB = ['459551209#3_1','459551209#3_0','459551209#3_2','459551209#3_3','459551209#0_0','459551209#0_1','459551209#0_2','459551209#0_3']
    
list(NAME.loc[BACKLOG['KASEMRAT_WB'],"id"])+KASEMRAT_EB


# In[26]:


def get_reward(alpha,beta):
    KASEMRAT_EB = ['459551209#3_1','459551209#3_0','459551209#3_2','459551209#3_3','459551209#0_0','459551209#0_1','459551209#0_2','459551209#0_3']
    
    ATTHAKAVI_KASEMRAT_EB = ['820340552#2_0','820340552#2_1','820340552#2_2','820340552#1_0','820340552#1_1','820340552#1_2','820340552#0_0','820340552#0_1','820340552#0_2','153225678#3_0','153225678#3_1','153225678#3_2','153225678#3_3','153225678#2_0','153225678#2_1','153225678#0_2','153225678#2_2','153225678#2_3','153225678#1_0','153225678#1_1','153225678#1_2','153225678#1_3','153225678#1-AddedOnRampEdge_0','153225678#1-AddedOnRampEdge_1','153225678#1-AddedOnRampEdge_2','153225678#1-AddedOnRampEdge_3','153225678#1-AddedOnRampEdge_4','153225678#0_0','153225678#0_1','153225678#0_3']
    max_throughput = 60
    max_backlog = sum([traci.lanearea.getLength(NAME.loc[k,"id"]) for i in BACKLOG.keys() for k in BACKLOG[i]])/(2.37+4.62)
#     print(max_backlog )
    throughput = 0
    throughput_KLONGTEI = 0
    throughput_KASEMRAT = 0
    throughput_NARANONG = 0
    throughput_SUNLAKAKHON = 0
    throughput_RAMA4 = 0
    throughput_ATTHAKAVI_RAMA4 = 0
    for i in range(15):
        traci.simulationStep()
        throughput += get_throughput(ALL_loopcoil)
        throughput_KLONGTEI += get_throughput(KLONGTEI_loopcoil)
        throughput_KASEMRAT += get_throughput(KASEMRAT_loopcoil)
        throughput_NARANONG += get_throughput(NARANONG_loopcoil)
        throughput_SUNLAKAKHON += get_throughput(SUNLAKAKHON_loopcoil)
        throughput_RAMA4 += get_throughput(RAMA4_loopcoil)
        throughput_ATTHAKAVI_RAMA4 += get_throughput(ATTHAKAVI_RAMA4_loopcoil)
    
    drawback = get_drawback(NAME.loc[:,'id'])
    drawback_GRIDLOCKAREA = get_drawback(GRIDLOCKAREA)
    rewards = throughput - alpha*drawback #+ beta*drawback_GRIDLOCKAREA 
    reward={}
    reward[0] = beta*throughput_KLONGTEI/max_throughput  - alpha*get_drawback(NAME.loc[BACKLOG['KLONGTEI_NB']+BACKLOG['KLONGTEI_EB']+BACKLOG['KLONGTEI_WB'],'id'])/max_backlog
    reward[1] = beta*throughput_RAMA4/max_throughput  - alpha*get_drawback(NAME.loc[BACKLOG['RAMA4_EB']+BACKLOG['RAMA4_NB']+BACKLOG['RAMA4_WB']+BACKLOG['RAMA4_SB'],'id'])/max_backlog
    reward[2] = beta*throughput_NARANONG/max_throughput  - alpha*get_drawback(NAME.loc[BACKLOG['NARANONG_NB']+BACKLOG['NARANONG_EB']+BACKLOG['NARANONG_SW']+BACKLOG['NARANONG_SB']+BACKLOG['NARANONG_WB'],'id'])/max_backlog
    reward[3] = beta*throughput_SUNLAKAKHON/max_throughput  - alpha*get_drawback(NAME.loc[BACKLOG['SUNLAKAKHON_EB']+BACKLOG['SUNLAKAKHON_NB']+BACKLOG['SUNLAKAKHON_WB']+BACKLOG['SUNLAKAKHON_SB'],'id'])/max_backlog
    reward[4] = beta*throughput_KASEMRAT/max_throughput  - alpha*get_drawback(KASEMRAT_EB+list(NAME.loc[BACKLOG['KASEMRAT_WB']+BACKLOG['KASEMRAT_NB'],'id']))/max_backlog
    reward[5] = beta*throughput_ATTHAKAVI_RAMA4/max_throughput  - alpha*get_drawback(ATTHAKAVI_KASEMRAT_EB+list(NAME.loc[BACKLOG['MASUKGRIDLOCK_ARI']+BACKLOG['MASUKGRIDLOCK_MASUK']+BACKLOG['MASUKGRIDLOCK_ATTHAKAWI']+                                                                         BACKLOG['MASUKGRIDLOCK_SUKHUMVIT22']+BACKLOG['MASUKGRIDLOCK_SUKHUMVIT24']+BACKLOG['MASUKGRIDLOCK_SUKHUMVIT26'],'id']))/max_backlog
            
     
    
    rewards = reward[0]+reward[1]+reward[2]+reward[3]+reward[4]+reward[5]
#     drawback_GRIDLOCKAREA = get_drawback(GRIDLOCKAREA)
#     rewards = throughput - alpha*drawback + beta*drawback_GRIDLOCKAREA 
#     reward={}
#     reward[0] = throughput_KLONGTEI - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA/6
#     reward[1] = throughput_RAMA4 - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA/6
#     reward[2] = throughput_NARANONG - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA/6
#     reward[3] = throughput_SUNLAKAKHON - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA /6
#     reward[4] = throughput_KASEMRAT - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA /6
#     reward[5] = throughput_ATTHAKAVI_RAMA4 - alpha*drawback/6 + beta*drawback_GRIDLOCKAREA/6
     
    return rewards, throughput, drawback, reward 


# In[27]:


number_phase = [4,9,7,5,4,3]
def set_current_phase(action, current_phase):

    if action[0] < 4:
        phase = action[0]
        current_phase[0] = phase
    if action[1] < 9:
        phase = action[1]
        current_phase[1] = phase
    if action[2] < 7:
        phase = action[2]
        current_phase[2] = phase
    if action[3] < 5:
        phase = action[3]
        current_phase[3] = phase
    if action[4] < 4:
        phase = action[4]
        current_phase[4] = phase
    if action[5] < 3:
        phase = action[5]
        current_phase[5] = phase
    for i in range (6):
        traci.trafficlight.setPhase(junction_id[junction_name[i]], current_phase[i])
    
    if current_phase[5] == 2:
        traci.lane.setAllowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_1_0_LSXT', 'id'], ['passenger'])
        traci.lane.setAllowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_2_0_LXXX', 'id'], ['passenger'])
        traci.lane.setAllowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_0_0_XSRT', 'id'], ['passenger'])
    elif current_phase[5] == 1:
        traci.lane.setDisallowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_1_0_LSXT', 'id'], ['passenger'])         
        traci.lane.setDisallowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_2_0_LXXX', 'id'], ['passenger'])
        traci.lane.setDisallowed(NAME.loc['MASUKGRIDLOCK_ATTHAKAWI_SB_0_0_XSRT', 'id'], ['passenger'])
    return


# In[28]:


from ray.rllib.env.multi_agent_env import MultiAgentEnv
class MyEnv3(MultiAgentEnv):
    def __init__(self, return_agent_actions = False, part=False):
        
        self.alpha = env_config['alpha']
        self.beta = env_config['beta']
        self.name = env_config['name'] # for pickle
        self.nearkill = 0
        self.num_agents = 6
        self.observation_space = gym.spaces.Box(low=0, high=20000, shape=(62,), dtype=np.float16)
#         self.action_space = gym.spaces.Discrete(9)
#         self.action_space = gym.spaces.MultiDiscrete(np.array([4,9,7,5,4,3]))
#     gym.spaces.Box(low=np.array([0,0,0,0,0,0]), high=np.array([4,9,7,5,4,3]), dtype=np.int8)
        self.episode = 0
        self.count = 0
        self.reward = 0
        self.rewards = 0
        self.throughputs = 0
        self.drawbacks = 0
        self.current_phase = [1,1,1,1,1,1]
        self.done = False
        self.reward_memory = []
        self.log_action = []
#         self.action_space = gym.spaces.Discrete(32)
        self.dateTimeObj = ''
        print(self.dateTimeObj)
        with open( "./Raytest/ray_results/result"+self.name+".csv" , 'w', newline='') as csv_file:
                header = ['rewards', 'throughput','backlog',"meanWaitingTime", "meanTravelTime","meanSpeed","action"]
                writer = csv.DictWriter(csv_file, fieldnames = header)
                writer.writeheader()         
    def reset(self):
        self.nearkill = 0
        self.episode += 1
        self.log_action = []
        self.reward_memory.append(self.rewards)
        self.count = 0
        self.meanspeed = 0
        dateTimeObj = datetime.datetime.now()
        self.dateTimeObj = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
#         print(type(self.dateTimeObj))
        start(self.dateTimeObj)
        self.reward = 0
        self.rewards = 0
        self.throughputs = 0
        self.backlogs = 0
        print(self.reward_memory)
        current_phase, hot_encoding_current_phase = get_hot_encoding_current_phase()
        state = get_state_attention(current_phase, hot_encoding_current_phase)
#         print(state)
        self.done = False
        self.current_phase = current_phase
        if len(self.reward_memory)%100 == 0:
            print('memory',self.reward_memory[-10:])
        return state
    def step(self, action):
        done = {}
        set_current_phase(action, self.current_phase)
#         print(action)
        current_phase, hot_encoding_current_phase = get_hot_encoding_current_phase()
        rewards, throughput, drawback, reward = get_reward(self.alpha,self.beta)
        self.rewards += rewards
        self.throughputs += throughput
        self.backlogs += drawback
        self.meanspeed += get_mean_speed()
        state = get_state_attention(current_phase, hot_encoding_current_phase)
        if np.isnan(self.reward) == True:
            print('HELP', type(self.reward))
        self.count += 1
        self.current_phase = current_phase
        self.log_action.append([str(action[key]) for key in action.keys()])
#         print('count', self.count)
        self.done = False
        done[0] = False
        done[1] = False
        done[2] = False
        done[3] = False
        done[4] = False
        done[5] = False
        done["__all__"] = False
#         if get_mean_speed() <= 2:
#             self.nearkill += 1
#         else:
#             self.nearkill = 0
#         if get_mean_speed() <= 2 and self.count >= 50 and self.nearkill > 10: #2880
#             self.nearkill = 0
#             traci.close()
# #             self.rewards -= 100000
# #             self.reward -= 100000
#             self.done = True
#             done[0] = True
#             done[1] = True
#             done[2] = True
#             done[3] = True
#             done[4] = True
#             done[5] = True
#             done["__all__"] = True
#             meanWaitingTime_avg = 0
#             meanTravelTime_avg = 0
#             meanSpeed_avg = 0
# #             meanWaitingTime_avg,meanTravelTime_avg,meanSpeed_avg = read_summary_xml(self.dateTimeObj)
#             data_set = {"rewards": self.rewards, "meanWaitingTime": meanWaitingTime_avg, "meanTravelTime": meanTravelTime_avg,
#                        "meanSpeed": meanSpeed_avg, "throughput": self.throughputs, "backlog": self.backlogs/2880, 
#                         "action":self.log_action
#                        }
            
#             self.json_dump = json.dumps(data_set)
# #             if self.episode%20 == 0:
# #                 self.log_action_json = json.dumps(self.log_action)
# #                 with open( "./Raytest/ray_results/action"+self.dateTimeObj+".csv" , 'a', newline='') as csv_file:
# #                     header = ['action']
# #                     writer = csv.DictWriter(csv_file, fieldnames = header)
# #                     writer.writerow({'action': self.log_action})
                                 
#             with open( "./Raytest/ray_results/result"+"MULTIAGENTAPEX_ROAD_jam"+".csv" , 'a', newline='') as csv_file:
#                 header = ['rewards', 'throughput','backlog',"meanWaitingTime", "meanTravelTime","meanSpeed","action"]
#                 writer = csv.DictWriter(csv_file, fieldnames = header)
#                 writer.writerow({'rewards': self.rewards, 
#                                  'throughput': self.throughputs,
#                                 'backlog': self.backlogs/2880,
#                                 "meanWaitingTime": meanWaitingTime_avg, "meanTravelTime": meanTravelTime_avg,
#                        "meanSpeed": meanSpeed_avg, "action":self.log_action})

        if self.count >= 960: #2880
            self.nearkill = 0
            traci.close()
            self.done = True
            done[0] = True
            done[1] = True
            done[2] = True
            done[3] = True
            done[4] = True
            done[5] = True
            done["__all__"] = True
            meanWaitingTime_avg = 0
            meanTravelTime_avg = 0
            meanSpeed_avg = 0
#             meanWaitingTime_avg,meanTravelTime_avg,meanSpeed_avg = read_summary_xml(self.dateTimeObj)
            data_set = {"rewards": self.rewards, "meanWaitingTime": meanWaitingTime_avg, "meanTravelTime": meanTravelTime_avg,
                       "meanSpeed": self.meanspeed, "throughput": self.throughputs, "backlog": self.backlogs, 
                        "action":self.log_action
                       }
            
            self.json_dump = json.dumps(data_set)
            send_to_peam1(self.json_dump,self.name)
#             if self.episode%20 == 0:
#                 self.log_action_json = json.dumps(self.log_action)
#                 with open( "./Raytest/ray_results/action"+self.dateTimeObj+".csv" , 'a', newline='') as csv_file:
#                     header = ['action']
#                     writer = csv.DictWriter(csv_file, fieldnames = header)
#                     writer.writerow({'action': self.log_action})
                                 
            with open( "./Raytest/ray_results/result"+self.name+".csv" , 'a', newline='') as csv_file:
                header = ['rewards', 'throughput','backlog',"meanWaitingTime", "meanTravelTime","meanSpeed","action"]
                writer = csv.DictWriter(csv_file, fieldnames = header)
                writer.writerow({'rewards': self.rewards, 
                                 'throughput': self.throughputs,
                                'backlog': self.backlogs/960,
                                "meanWaitingTime": meanWaitingTime_avg, "meanTravelTime": meanTravelTime_avg,
                       "meanSpeed": self.meanspeed/960, "action":self.log_action})

        
#         return_state = np.array(state).astype(np.float16)
        
#         print(return_state)
#         info = {"throughput": throughput,
#                 "drawback":drawback
#                 }
#         info = {**info}
#         print(info)
        return state , reward, done, {}


# In[29]:


from ray.tune import Callback
class MyCallback(Callback):
    def on_trial_start(self, iteration, trials, trial, **info):
        print(f"I am in callback. This is iteration {iteration} inside trial {trial}")
#         dateTimeObj = datetime.datetime.now()
#         dateTimeObj = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
#         with open( "./Raytest/ray_results/"+dateTimeObj+".csv" , 'a', newline='') as csv_file:
#                 header = ['rewards', 'throughput','drawback']
#                 writer = csv.DictWriter(csv_file, fieldnames = header)
#                 writer.writeheader()
#         print(info)
    def on_trial_result(self, iteration, trials, trial, result, **info):
        print("I am in second callback. Got result:", info)
        send_to_peam2(str(trials))
#         with open( "./Raytest/ray_results/"+str(trial)+".csv" , 'a', newline='') as csv_file:
#             header = ['rewards']
#             writer = csv.DictWriter(csv_file, fieldnames = header)
#             writer.writeheader()
#             writer.writerow({'rewards': result["episode_reward_mean"]})


# In[30]:


import ray
from ray import tune
from ray.rllib.agents.registry import get_agent_class
from ray.rllib.models import ModelCatalog
from ray.tune import run_experiments
from ray.tune.registry import register_env
from ray.rllib.agents.dqn.apex import ApexTrainer


# In[25]:


def env_creator(_):
    return MyEnv3()


from ray.rllib.agents.dqn.dqn import calculate_rr_weights,     DEFAULT_CONFIG as DQN_CONFIG, DQNTrainer, validate_config
from ray.rllib.utils import merge_dicts
def peam_ok(test_id, data_json):
    json_string = str(data_json)
    option = json.loads(json_string)
    global env_config
    env_config =  {"alpha": option["alpha"], "beta" : option["beta"] , "name" : test_id
                    }
    single_env = MyEnv3()
    env_name = "MyEnv3"
    register_env(env_name, env_creator)

    # Get environment obs, action spaces and number of agents
    obs_space = single_env.observation_space
    act_space = [4,9,7,5,4,3]
    num_agents = single_env.num_agents

    # Create a policy mapping
    def gen_policy(i):
        return (None, obs_space, gym.spaces.Discrete(act_space[i]), {})

    policy_graphs = {}
    for i in range(num_agents):
        policy_graphs['agent-' + str(i)] = gen_policy(i)

    def policy_mapping_fn(agent_id):
        return 'agent-' + str(agent_id)
    config={
                "log_level": 'WARNING' ,
                "adam_epsilon": 1e-8,
                "noisy": True,
                "optimizer": merge_dicts(
                    DQN_CONFIG["optimizer"], {
                        "max_weight_sync_delay": 400,
                        "num_replay_buffer_shards": 4,
                        "debug": False
            }),
                # If not None, clip gradients during optimization at this value

                "num_gpus": 0,
                "dueling": True,
                "double_q": True,
                "num_workers": 31,
                "buffer_size": 100000,
                "framework": "tf",
                "learning_starts": 9600, #2160
                "train_batch_size": 960,
        #             "num_samples": 20,
                "rollout_fragment_length": 50,
                "target_network_update_freq": 9600,
                "prioritized_replay": True,
                "timesteps_per_iteration": 3840, #2880
                "exploration_config": {"type": "PerWorkerEpsilonGreedy",
                                       "initial_epsilon": 1.0,
                                        "final_epsilon": 0.1,
                                        "epsilon_timesteps": 150000,  # Timesteps over which to anneal epsilon.
                                        },
                "worker_side_prioritization": True,
        #         "min_iter_time_s": 30,
                # If set, this will fix the ratio of replayed from a buffer and learned
                # on timesteps to sampled from an environment and stored in the replay
                # buffer timesteps. Otherwise, replay will proceed as fast as possible.
        #         "training_intensity": None,
                 "lr": option["lr"],
                "gamma":option["gamma"],
                "num_cpus_for_driver": 1,
                "num_cpus_per_worker": 1,
                "num_gpus" : 0,
#                 "model":{"fcnet_hiddens": [8, 8]},
                "multiagent": {
                    "policies": policy_graphs,
                    "policy_mapping_fn": policy_mapping_fn,
                },
                "env": MyEnv3,
                "env_config" : {"alpha": option["alpha"], "beta" : option["beta"] , "name" : test_id
                       }}

    # Define experiment details
    exp_name = 'my_exp5'
    exp_dict = {
        'name': exp_name,
        'run_or_experiment': 'APEX',
    #             "stop": {
    #                 "training_iteration": 100
    #             },
         'local_dir' : "/Raytest/ray_results/",
        'checkpoint_at_end' : True,
        'log_to_file' : True,
        'checkpoint_freq': 20,
        "config": config,
#         "callbacks": [MyCallback()]
    #     "restore":"/Raytest/Raytest/ray_results/my_exp3/APEX_MyEnv3_22fea_00000_0_2021-04-13_00-42-34/checkpoint_90/checkpoint-90"
    }

    # Initialize ray and run
    ray.shutdown()
    ray.init()
    results = tune.run(**exp_dict)


# In[ ]:


peam_ok(test_id, data_json)


# In[ ]:


len([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
       0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.])


# In[ ]:




