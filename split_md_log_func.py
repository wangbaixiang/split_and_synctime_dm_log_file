#!/usr/bin/python
"""
    1 find out all diag_log_<timestemp>.txt files under ./ by call readAllMdLogFiles(".", fileNames)
    2 split diag_log_<timestemp>.txt and sync each line timestemp by the file's timestemp to diag_log_<timestemp>_X_split.log 
"""

import os
from datetime import datetime
import time


def split_and_synctime_dm_log_file(md_log_name):
    source_file_name = md_log_name
    destination_file_name = source_file_name.replace(".txt","_");

    SINGLE_FILE_LINE_MAX = 1200000
    single_file_line = 0
    file_cnt = 0
    
    dump_split_line_level = False
    i = 0;j = 0
    TIMER = 2000000

    print("split "+ source_file_name + " start at:" + time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))
    # ref https://www.crifan.com/python_strftime_format_datetime-2/
    #d1 = datetime.strptime("20200722_190848159", "%Y%m%d_%H%M%S%f")
    d1 = datetime.strptime(source_file_name[11:32], "%Y%m%d_%H%M%S%f")
    local_dt = None
    dlt_dt = None
    is_first_dt = True

    out_file = open(destination_file_name + str(file_cnt) + "_split.log", 'w', encoding='UTF-8')
    print("split new file:", out_file.name)
    with open(source_file_name, 'r', encoding='UTF-8') as in_file:
        for line in in_file:
            if line in ['\n','\r\n', '}\n',' \n','	Drop count = 0\n', 'Data = { \n']:
                pass
            else:
                line = line.replace("  0x1FEB  Extended Debug Message\n","", 1)

                if line.startswith("1980"):
                    dm_dt_str = line[0:25]
                    dm_dt = datetime.strptime(dm_dt_str, "%Y %b %d %H:%M:%S.%f")

                    if is_first_dt:
                        dlt_dt = d1 - dm_dt
                        is_first_dt = False

                    local_dt = dm_dt + dlt_dt
                    line = line.replace(dm_dt_str, local_dt.isoformat())

                if single_file_line == SINGLE_FILE_LINE_MAX:
                    file_cnt += 1
                    single_file_line = 0
                    out_file.close()
                    if local_dt == None:
                        out_file = open(destination_file_name + str(file_cnt) + "_split.log", 'w', encoding='UTF-8')
                    else:
                        out_file = open(destination_file_name + str(file_cnt) + "_" + local_dt.strftime('%H%M%S.%f') + "_split.log", 'w', encoding='UTF-8')
                    print("split new file:", out_file.name)

                out_file.write(line)
                single_file_line = single_file_line + 1

                if dump_split_line_level:
                    i = i+1
                    if i == TIMER:
                        j=j+1
                        i=0
                        print("dump line", j*TIMER)
    out_file.close()
    print("split " +source_file_name+ " end at:"+ time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())))

def readAllMdLogFiles(filePath, fileNames):
    fileList = os.listdir(filePath)
    for file in fileList:
        path = os.path.join(filePath, file)
        if os.path.isfile(path)& path.startswith(".\diag_log_") & path.endswith(".txt") :
            print("dm log:",path)
            fileNames.append(path)

print("split start")
fileNames = []
readAllMdLogFiles(".", fileNames)
for filename in fileNames:
    split_and_synctime_dm_log_file(filename)
print("split end")