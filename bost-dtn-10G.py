"""
BOST-DTN ANALYSIS

1. ALL HOSTS
2. ESNET HOSTS
3. NON-ESNET HOSTS
"""

import os
import json
import numpy as np
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

rootdir = "/Users/eashan22/Desktop/Internship 2021/bbrv2/Brian's Project/bost-dtn-10G/"

def traverse(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.startswith("ss") and file.endswith("json"):
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"Total files: {c}")
    return fileList

def traverse_esnet(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.startswith("ss") and file.endswith("json") and file.find("es.net")!=-1: # esnet host
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"Total files: {c}")
    return fileList

def traverse_non_esnet(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.startswith("ss") and file.endswith("json") and file.find("es.net")==-1: # non-esnet host
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"Total files: {c}")
    return fileList


paths = [
    (
        "2021-08-02:23:01/pscheduler_bbr2_p1",
        "2021-08-02:23:01/pscheduler_bbr2_p16"
    ),
    (
        "2021-08-02:23:01/pscheduler_cubic_p1",
        "2021-08-02:23:01/pscheduler_cubic_p16"
    ),
    (
        "2021-07-30:19:21/pscheduler_both_p16",
        "2021-07-31:04:13/pscheduler_both_p16",
        "2021-07-31:14:26/pscheduler_both_p16",
        "2021-08-02:23:01/pscheduler_both_p16",
        "10G-to-ESnet/pscheduler_both_p16",
    )
]

print("\n")
print(50*"=")
print("ESNET HOSTS")
print(50*"=")
print("\n")

if not len(paths[0])==0:
    for q1 in paths[0]:
        print(f"=== {q1} ===")
        pscheduler_bbr2  = os.path.join(rootdir, q1)
        filenames = traverse_esnet(pscheduler_bbr2)

        data_seg = []
        tput_bbr2_p1 = []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                data = [json.loads(line) for line in open(f, 'r')]

                bbr2_data_seg, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in enumerate(data):
                    if "interval" in d.keys() and j==0:
                        start_time = data[j]['interval']['time'] # Start time of the test
                    elif key2 in data[j].keys():
                        end_time = data[j-1]['interval']['time'] # End time of the test
                        mss = data[j-1]['interval']['mss'] # maximum segment size

                        bbr2_data_seg = data[j][key2]
                        data_seg.append( bbr2_data_seg )

                        throughput = (bbr2_data_seg*mss*8)/(end_time-start_time)/1e9
                        tput_bbr2_p1.append( throughput )

            except Exception as e:
                print(e)

        print("Throughput (P1)")
        print(f"BBRv2 - M, C.V : {np.mean(tput_bbr2_p1):.4f}, {(np.std(tput_bbr2_p1)/np.mean(tput_bbr2_p1)):.4f}")
        print("")

if not len(paths[1])==0:
    for q2 in paths[1]:
        print(f"=== {q2} ===")
        pscheduler_cubic = os.path.join(rootdir, q2)
        filenames = traverse_esnet(pscheduler_cubic)

        data_seg = []
        tput_p1_cubic = []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                # The MongoDB JSON dump has one object per line, so this works for me.
                data = [json.loads(line) for line in open(f, 'r')]

                cubic_data_seg, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in enumerate(data):
                    if "interval" in d.keys() and j==0:
                        start_time = data[j]['interval']['time'] # Start time of the test
                    elif key1 in data[j].keys():
                        end_time = data[j-1]['interval']['time'] # End time of the test
                        mss = data[j-1]['interval']['mss'] # maximum segment size

                        cubic_data_seg = data[j][key1]
                        data_seg.append( cubic_data_seg )

                        throughput = (cubic_data_seg*mss*8)/(end_time-start_time)/1e9
                        tput_p1_cubic.append( throughput )

            except Exception as e:
                print(e)

        print("Throughput (P1)")
        print(f"CUBIC - M, C.V : {np.mean(tput_p1_cubic):.4f}, {(np.std(tput_p1_cubic)/np.mean(tput_p1_cubic)):.4f}")
        print("")

if not len(paths[2])==0:
    for q3 in paths[2]:
        print(f"=== {q3} ===")
        pscheduler_both = os.path.join(rootdir, q3)
        filenames = traverse_esnet(pscheduler_both)

        data_seg_sum_cubic, data_seg_sum_bbr2 = [], []
        tput_cubic_p16, tput_bbr2_p16 = [], []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                data = [json.loads(line) for line in open(f, 'r')]

                throughput_cubic, throughput_bbr2, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in zip(range(len(data)),data):
                    try:
                        if "interval" in d.keys() and j==0:
                            start_time = d['interval']['time'] # Start time of the test
                        if "streams" in d.keys():
                            end_time = data[j-1]['interval']['time'] # End time of the test
                            mss = data[j-1]['interval']['mss'] # maximum segment size

                            cubic_data_seg_list, bbr2_data_seg_list = [], []
                            for j in range(len(d['streams'])):
                                if "cubic" in d['streams'][j]['cc']:
                                    cubic_data_seg_list.append(d['streams'][j]['data_segs'])
                                elif "bbr2" in d['streams'][j]['cc']:
                                    bbr2_data_seg_list.append(d['streams'][j]['data_segs'])

                            data_seg_sum_cubic.append( sum(cubic_data_seg_list) )
                            throughput_cubic = (sum(cubic_data_seg_list)*mss*8)/(end_time-start_time)/1e9
                            tput_cubic_p16.append( throughput_cubic )

                            data_seg_sum_bbr2.append( sum(bbr2_data_seg_list) )
                            throughput_bbr2 = (sum(bbr2_data_seg_list)*mss*8)/(end_time-start_time)/1e9
                            tput_bbr2_p16.append( throughput_bbr2 )

                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)

        print("Throughput (P16)")
        print(f"BBRv2 - M, C.V : {np.mean(tput_bbr2_p16):.4f}, {(np.std(tput_bbr2_p16)/np.mean(tput_bbr2_p16)):.4f}")
        print(f"CUBIC - M, C.V : {np.mean(tput_cubic_p16):.4f}, {(np.std(tput_cubic_p16)/np.mean(tput_cubic_p16)):.4f}")
        print("")

# ============================================================================
print("\n")
print(50*"=")
print("NON-ESNET HOSTS")
print(50*"=")


print("\n")
if not len(paths[0])==0:
    for q1 in paths[0]:
        print(f"=== {q1} ===")
        pscheduler_bbr2  = os.path.join(rootdir, q1)
        filenames = traverse_non_esnet(pscheduler_bbr2)

        data_seg = []
        tput_bbr2_p1 = []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                data = [json.loads(line) for line in open(f, 'r')]

                bbr2_data_seg, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in enumerate(data):
                    if "interval" in d.keys() and j==0:
                        start_time = data[j]['interval']['time'] # Start time of the test
                    elif key2 in data[j].keys():
                        end_time = data[j-1]['interval']['time'] # End time of the test
                        mss = data[j-1]['interval']['mss'] # maximum segment size

                        bbr2_data_seg = data[j][key2]
                        data_seg.append( bbr2_data_seg )

                        throughput = (bbr2_data_seg*mss*8)/(end_time-start_time)/1e9
                        tput_bbr2_p1.append( throughput )

            except Exception as e:
                print(e)

        print("Throughput (P1)")
        print(f"BBRv2 - M, C.V : {np.mean(tput_bbr2_p1):.4f}, {(np.std(tput_bbr2_p1)/np.mean(tput_bbr2_p1)):.4f}")
        print("")

if not len(paths[1])==0:
    for q2 in paths[1]:
        print(f"=== {q2} ===")
        pscheduler_cubic = os.path.join(rootdir, q2)
        filenames = traverse_non_esnet(pscheduler_cubic)

        data_seg = []
        tput_p1_cubic = []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                # The MongoDB JSON dump has one object per line, so this works for me.
                data = [json.loads(line) for line in open(f, 'r')]

                cubic_data_seg, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in enumerate(data):
                    if "interval" in d.keys() and j==0:
                        start_time = data[j]['interval']['time'] # Start time of the test
                    elif key1 in data[j].keys():
                        end_time = data[j-1]['interval']['time'] # End time of the test
                        mss = data[j-1]['interval']['mss'] # maximum segment size

                        cubic_data_seg = data[j][key1]
                        data_seg.append( cubic_data_seg )

                        throughput = (cubic_data_seg*mss*8)/(end_time-start_time)/1e9
                        tput_p1_cubic.append( throughput )

            except Exception as e:
                print(e)

        print("Throughput (P1)")
        print(f"CUBIC - M, C.V : {np.mean(tput_p1_cubic):.4f}, {(np.std(tput_p1_cubic)/np.mean(tput_p1_cubic)):.4f}")
        print("")

if not len(paths[2])==0:
    for q3 in paths[2]:
        print(f"=== {q3} ===")
        pscheduler_both = os.path.join(rootdir, q3)
        filenames = traverse_non_esnet(pscheduler_both)

        data_seg_sum_cubic, data_seg_sum_bbr2 = [], []
        tput_cubic_p16, tput_bbr2_p16 = [], []
        key1, key2, key3 = 'cubic_data_segs', 'bbr2_data_segs', 'bbr_data_segs'

        for i,f in enumerate(filenames):
            try:
                path = Path(f)
                data = [json.loads(line) for line in open(f, 'r')]

                throughput_cubic, throughput_bbr2, throughput, mss, start_time, end_time = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                for j,d in zip(range(len(data)),data):
                    try:
                        if "interval" in d.keys() and j==0:
                            start_time = d['interval']['time'] # Start time of the test
                        if "streams" in d.keys():
                            end_time = data[j-1]['interval']['time'] # End time of the test
                            mss = data[j-1]['interval']['mss'] # maximum segment size

                            cubic_data_seg_list, bbr2_data_seg_list = [], []
                            for j in range(len(d['streams'])):
                                if "cubic" in d['streams'][j]['cc']:
                                    cubic_data_seg_list.append(d['streams'][j]['data_segs'])
                                elif "bbr2" in d['streams'][j]['cc']:
                                    bbr2_data_seg_list.append(d['streams'][j]['data_segs'])

                            data_seg_sum_cubic.append( sum(cubic_data_seg_list) )
                            throughput_cubic = (sum(cubic_data_seg_list)*mss*8)/(end_time-start_time)/1e9
                            tput_cubic_p16.append( throughput_cubic )

                            data_seg_sum_bbr2.append( sum(bbr2_data_seg_list) )
                            throughput_bbr2 = (sum(bbr2_data_seg_list)*mss*8)/(end_time-start_time)/1e9
                            tput_bbr2_p16.append( throughput_bbr2 )

                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)

        print("Throughput (P16)")
        print(f"BBRv2 - M, C.V : {np.mean(tput_bbr2_p16):.4f}, {(np.std(tput_bbr2_p16)/np.mean(tput_bbr2_p16)):.4f}")
        print(f"CUBIC - M, C.V : {np.mean(tput_cubic_p16):.4f}, {(np.std(tput_cubic_p16)/np.mean(tput_cubic_p16)):.4f}")
        print("")



