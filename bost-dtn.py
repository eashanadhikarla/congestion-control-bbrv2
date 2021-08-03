"""
BOST-DTN ANALYSIS

1. ALL HOSTS
2. ESNET HOSTS
3. NON-ESNET HOSTS
"""

import os
import json
import numpy as np
from pathlib import Path

rootdir = "/Users/eashan22/Desktop/Internship 2021/bbrv2/Brian's Project/bost-dtn"


def traverse1(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.endswith("json"):
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"total files: {c}")
    return fileList

paths = [("2021-06-09:14:35/pscheduler_bbr2_p1", "2021-06-09:14:35/pscheduler_cubic_p1", "2021-06-09:14:35/pscheduler_both_p16"),
         ("2021-06-15:02:12/pscheduler_bbr2_p1", "2021-06-15:02:12/pscheduler_cubic_p1", "2021-06-15:02:12/pscheduler_both_p16"),
         ("2021-06-16:02:12/pscheduler_bbr2_p1", "2021-06-16:02:12/pscheduler_cubic_p1", "2021-06-16:02:12/pscheduler_both_p16")
        ]

print(50*"=")
print("1. ALL HOSTS")
print(50*"=")
for p in paths:
    print(f"--- {p} ---")
    pscheduler_bbr2  = os.path.join(rootdir, p[0])
    filenames = traverse1(pscheduler_bbr2)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p1):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p1):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p1)/np.mean(tput_bbr2_p1)):.5f}  |  Variance: {np.var(tput_bbr2_p1):.5f}")
    print("Data Segment (P1)")
    print(f"BBRv2 - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_cubic = os.path.join(rootdir, p[1])
    filenames = traverse1(pscheduler_cubic)

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
    print(f"CUBIC - Mean: {np.mean(tput_p1_cubic):.5f}  |  Std. Dev.: {np.std(tput_p1_cubic):.5f}  |  Coef. of Variance: {(np.std(tput_p1_cubic)/np.mean(tput_p1_cubic)):.5f}  |  Variance: {np.var(tput_p1_cubic):.5f}")
    print("Data Segment (P1)")
    print(f"CUBIC - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_both = os.path.join(rootdir, p[2])
    filenames = traverse1(pscheduler_both)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p16):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p16):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p16)/np.mean(tput_bbr2_p16)):.5f}  |  Variance: {np.var(tput_bbr2_p16):.5f}")
    print(f"CUBIC - Mean: {np.mean(tput_cubic_p16):.5f}  |  Std. Dev.: {np.std(tput_cubic_p16):.5f}  |  Coef. of Variance: {(np.std(tput_cubic_p16)/np.mean(tput_cubic_p16)):.5f}  |  Variance: {np.var(tput_cubic_p16):.5f}")

    print("Data Segment (P16)")
    print(f"BBRv2 - Mean: {np.mean(data_seg_sum_bbr2):.5f}  |  Std. Dev.: {np.std(data_seg_sum_bbr2):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_bbr2)/np.mean(data_seg_sum_bbr2)):.5f}  |  Variance: {np.var(data_seg_sum_bbr2):.5f}")
    print(f"CUBIC - Mean: {np.mean(data_seg_sum_cubic):.5f}  |  Std. Dev.: {np.std(data_seg_sum_cubic):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_cubic)/np.mean(data_seg_sum_cubic)):.5f}  |  Variance: {np.var(data_seg_sum_cubic):.5f}")
    print(50*"=")


# =========================================================================================================================

def traverse2(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.endswith("json") and file.find("es.net")!=-1: # esnet host
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"total files: {c}")
    return fileList

paths = [("2021-06-09:14:35/pscheduler_bbr2_p1", "2021-06-09:14:35/pscheduler_cubic_p1", "2021-06-09:14:35/pscheduler_both_p16"),
         ("2021-06-15:02:12/pscheduler_bbr2_p1", "2021-06-15:02:12/pscheduler_cubic_p1", "2021-06-15:02:12/pscheduler_both_p16"),
         ("2021-06-16:02:12/pscheduler_bbr2_p1", "2021-06-16:02:12/pscheduler_cubic_p1", "2021-06-16:02:12/pscheduler_both_p16")
        ]

print(50*"=")
print("2. ESNET HOSTS")
print(50*"=")

for p in paths:
    print(f"--- {p} ---")
    pscheduler_bbr2  = os.path.join(rootdir, p[0])
    filenames = traverse2(pscheduler_bbr2)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p1):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p1):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p1)/np.mean(tput_bbr2_p1)):.5f}  |  Variance: {np.var(tput_bbr2_p1):.5f}")
    print("Data Segment (P1)")
    print(f"BBRv2 - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_cubic = os.path.join(rootdir, p[1])
    filenames = traverse2(pscheduler_cubic)

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
    print(f"CUBIC - Mean: {np.mean(tput_p1_cubic):.5f}  |  Std. Dev.: {np.std(tput_p1_cubic):.5f}  |  Coef. of Variance: {(np.std(tput_p1_cubic)/np.mean(tput_p1_cubic)):.5f}  |  Variance: {np.var(tput_p1_cubic):.5f}")
    print("Data Segment (P1)")
    print(f"CUBIC - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_both = os.path.join(rootdir, p[2])
    filenames = traverse2(pscheduler_both)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p16):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p16):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p16)/np.mean(tput_bbr2_p16)):.5f}  |  Variance: {np.var(tput_bbr2_p16):.5f}")
    print(f"CUBIC - Mean: {np.mean(tput_cubic_p16):.5f}  |  Std. Dev.: {np.std(tput_cubic_p16):.5f}  |  Coef. of Variance: {(np.std(tput_cubic_p16)/np.mean(tput_cubic_p16)):.5f}  |  Variance: {np.var(tput_cubic_p16):.5f}")

    print("Data Segment (P16)")
    print(f"BBRv2 - Mean: {np.mean(data_seg_sum_bbr2):.5f}  |  Std. Dev.: {np.std(data_seg_sum_bbr2):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_bbr2)/np.mean(data_seg_sum_bbr2)):.5f}  |  Variance: {np.var(data_seg_sum_bbr2):.5f}")
    print(f"CUBIC - Mean: {np.mean(data_seg_sum_cubic):.5f}  |  Std. Dev.: {np.std(data_seg_sum_cubic):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_cubic)/np.mean(data_seg_sum_cubic)):.5f}  |  Variance: {np.var(data_seg_sum_cubic):.5f}")
    print(50*"=")


# =========================================================================================================================

def traverse3(path):
    fileList = []
    c = 0
    for root, directories, files in os.walk(path):
        for file in files:
            if file.endswith("json") and file.find("es.net")==-1: # non-esnet host
                fileList.append(os.path.join(root,file))
                c+=1
    print(f"total files: {c}")
    return fileList

paths = [("2021-06-09:14:35/pscheduler_bbr2_p1", "2021-06-09:14:35/pscheduler_cubic_p1", "2021-06-09:14:35/pscheduler_both_p16"),
         ("2021-06-15:02:12/pscheduler_bbr2_p1", "2021-06-15:02:12/pscheduler_cubic_p1", "2021-06-15:02:12/pscheduler_both_p16"),
         ("2021-06-16:02:12/pscheduler_bbr2_p1", "2021-06-16:02:12/pscheduler_cubic_p1", "2021-06-16:02:12/pscheduler_both_p16")
        ]

print(50*"=")
print("3. NON-ESNET HOSTS")
print(50*"=")

for p in paths:
    print(f"--- {p} ---")
    pscheduler_bbr2  = os.path.join(rootdir, p[0])
    filenames = traverse3(pscheduler_bbr2)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p1):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p1):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p1)/np.mean(tput_bbr2_p1)):.5f}  |  Variance: {np.var(tput_bbr2_p1):.5f}")
    print("Data Segment (P1)")
    print(f"BBRv2 - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_cubic = os.path.join(rootdir, p[1])
    filenames = traverse3(pscheduler_cubic)

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
    print(f"CUBIC - Mean: {np.mean(tput_p1_cubic):.5f}  |  Std. Dev.: {np.std(tput_p1_cubic):.5f}  |  Coef. of Variance: {(np.std(tput_p1_cubic)/np.mean(tput_p1_cubic)):.5f}  |  Variance: {np.var(tput_p1_cubic):.5f}")
    print("Data Segment (P1)")
    print(f"CUBIC - Mean: {np.mean(data_seg):.5f}  |  Std. Dev.: {np.std(data_seg):.5f}  |  Coef. of Variance: {(np.std(data_seg)/np.mean(data_seg)):.5f}  |  Variance: {np.var(data_seg):.5f}")
    print("")

    pscheduler_both = os.path.join(rootdir, p[2])
    filenames = traverse3(pscheduler_both)

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
    print(f"BBRv2 - Mean: {np.mean(tput_bbr2_p16):.5f}  |  Std. Dev.: {np.std(tput_bbr2_p16):.5f}  |  Coef. of Variance: {(np.std(tput_bbr2_p16)/np.mean(tput_bbr2_p16)):.5f}  |  Variance: {np.var(tput_bbr2_p16):.5f}")
    print(f"CUBIC - Mean: {np.mean(tput_cubic_p16):.5f}  |  Std. Dev.: {np.std(tput_cubic_p16):.5f}  |  Coef. of Variance: {(np.std(tput_cubic_p16)/np.mean(tput_cubic_p16)):.5f}  |  Variance: {np.var(tput_cubic_p16):.5f}")

    print("Data Segment (P16)")
    print(f"BBRv2 - Mean: {np.mean(data_seg_sum_bbr2):.5f}  |  Std. Dev.: {np.std(data_seg_sum_bbr2):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_bbr2)/np.mean(data_seg_sum_bbr2)):.5f}  |  Variance: {np.var(data_seg_sum_bbr2):.5f}")
    print(f"CUBIC - Mean: {np.mean(data_seg_sum_cubic):.5f}  |  Std. Dev.: {np.std(data_seg_sum_cubic):.5f}  |  Coef. of Variance: {(np.std(data_seg_sum_cubic)/np.mean(data_seg_sum_cubic)):.5f}  |  Variance: {np.var(data_seg_sum_cubic):.5f}")
    print(50*"=")