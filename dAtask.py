#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:45:22 2018


Use taskwarrior to build the <Eisenhower's Urgency/Priority> table

@author: shullani
"""
import os
import commands
import json
import argparse
import numpy as np


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cT', '--collectTasks', help='Collect tasks from taskwarrior')
    parser.add_argument('-e', '--eisenTasks', help='Visualize eisen task in Urgency/Priority')
    return parser



# Export tasks from task warrior
def callTask(task_list_string):
    # 1. command: " task task_list_string export "
    cmd = "task {} export".format(task_list_string)
    status, output = commands.getstatusoutput(cmd)
    if status==0:
        # 2. parse and return json result
        #print(output)
        return json.loads(output)
    else:
        print(output)
     
        
# Build Eisenhower table 
def buildEisenStruct(json_tasks):
    # HL: High Priority - Low Urgency
    eisen_struct = {"HH":[], "HL":[], "LH":[], "LL":[]}
    data_list  = []
    # get max urgency
    urgency_list = [k["urgency"] for k in json_tasks]
    # H: max-2, L:min+2
    thresh = np.mean(urgency_list)
    
    # for each task define where to store it
    for item in json_tasks:
        
        # set N-priority if does not exist
        if not "priority" in item.keys():
            item["priority"] = "N"

        data_list.append(item)
        
        if (item["priority"]=="H" or item["priority"]=="M") and item["urgency"]>thresh :
            # HH - High Priority - High Urgency
            eisen_struct["HH"].append(item["id"])
        
        elif (item["priority"]=="H" or item["priority"]=="M") and item["urgency"]<= thresh:
            # HL - High Priority - Low Urgency
             eisen_struct["HL"].append(item["id"])
        elif (item["priority"]=="L" or item["priority"]=="N") and item["urgency"]>thresh :
            # LH - Low Priority - High Urgency
            eisen_struct["LH"].append(item["id"])
        elif (item["priority"]=="L" or item["priority"]=="N") and item["urgency"]<= thresh:
            # LL - Low Priority - Low Urgency
            eisen_struct["LL"].append(item["id"])
            
    return eisen_struct, data_list



if __name__=="__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.collectTasks is not None:
        #json_tasks = callTask("1,2,3,4,5,6,7,8,9,10")
        #
        #(eisen_struct, data) = buildEisenStruct(json_tasks)
        
        # get tasks and store data
        json_tasks = callTask(args.collectTasks)
        (eisen_struct, data) = buildEisenStruct(json_tasks)
        # write data
        with open('data_task.txt', 'w') as outfile:
            json.dump(data, outfile)
        #write eisen struct
        with open('eisen_task.txt', 'w') as outfile:
            json.dump(eisen_struct, outfile)
    if args.eisenTasks:
        currDir = os.getcwd()
        eisen_path = os.path.join(currDir, 'eisen_task.txt')
        data_path = os.path.join(currDir, 'data_task.txt')
        if os.path.exists(eisen_path) and os.path.exists(data_path):
            with open(eisen_path, 'r') as infile:
                eisen_data = json.load(infile)
                
            with open(data_path, 'r') as infile:
                task_data = json.load(infile)
            
            #TODO: print eisen table
            print eisen_data
        else:
            print "Eisenhower's Urgency/Priority table currently not available. Build one."
            exit 
 
        