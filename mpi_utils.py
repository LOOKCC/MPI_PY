#!usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import os
import mpi4py.MPI as MPI
import numpy as np

# Warning: This pipeline only support unordered file process, \
# because of multi-process can't guaranteed running order. 

# Usage
# First, install pkgs
# pip install mpi4py
# then use it. (-n for the number of process)
#  mpiexec -n 5 python  xxx.py

#
#  Global variables for MPI
#
 
# instance for invoking MPI relatedfunctions
comm = MPI.COMM_WORLD
# the node rank in the whole community
comm_rank = comm.Get_rank()
# the size of the whole community, i.e.,the total number of working nodes in the MPI cluster
comm_size = comm.Get_size()

# Place define your function
def function(line):
    # do what you want
    path, label = line.split()
    path = path.replace('DFDC_face_blaze_100', 'DFDC_face_blaze_100_frame')
    if os.path.exists(path):
        return path + ' 1\n'
    else:
        return path + ' 0\n'

 
if __name__ == '__main__':
    if comm_rank == 0:
        print("processor root starts reading data...\n")
        all_lines = open('/home/fanglingfei/workspace/DFDC/debug/train_face_100.txt', 'r').readlines()
    all_lines = comm.bcast(all_lines if comm_rank == 0 else None, root = 0)
    num_lines = len(all_lines)
    local_lines_offset = np.linspace(0, num_lines, comm_size +1).astype('int')
    local_lines = all_lines[local_lines_offset[comm_rank] :local_lines_offset[comm_rank + 1]]
    print("%d/%d processor gets %d/%d data \n" %(comm_rank, comm_size, len(local_lines), num_lines))
    cnt = 0
    send_data = []
    for line in local_lines:
        # process
        result = function(line)
        send_data.append(result)
        cnt += 1
        # if you want some information about every rank, place uncomment
        if cnt % 1000 == 0:
            print("processor %d has processed %d/%d lines \n" %(comm_rank, cnt, len(local_lines)))
    # get result
    recv_data = comm.gather(send_data, root=0)
    # save result  
    if comm_rank == 0:
        f = open('test.txt', 'w')
        for rank_result in recv_data:
            for line in rank_result:
                f.write(line)
    MPI.Finalize()
