import os
import sys
import subprocess
import pandas as pd
import time
import numpy as np

algs = ['RHC', 'SA', 'GA', 'MIMIC']

args = {}
maxN = 10
maxIters = 0
step = 1
a = 5

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if '-maxN' in sys.argv[i]:
            maxN = int(sys.argv[i+1])
        elif '-iters' in sys.argv[i]:
            maxIters = int(sys.argv[i+1])
        elif '-step' in sys.argv[i]:
            step = int(sys.argv[i+1])
        elif '-a' in sys.argv[i]:
            a = int(sys.argv[i+1])
else:
    exit()

file_name = ""

if not maxIters and a == 5:
    data = {'a': [], 'N': [], 't': [], 'time': [], 'score': []}
    file_name = "logs/WineExhaustive.log"
    for a in range(0, 4):
        for N in range(10, maxN+1, 10):
            for t in range(0, N, 5):
                print(str(a) + '\t' + str(N) + '\t' + str(t))
                data['a'].append(algs[a])
                data['N'].append(N)
                data['t'].append(t)
                time1 = time.time()
                proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.WineTest -a " + str(a) + 
                                        " -t " + str(t) + " -N " + str(N),
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = proc.communicate()
                time2 = time.time()
                data['time'].append((time2-time1) * 1000.0)
                data['score'].append(float(out.strip()))
elif a != 5:
    file_name = "logs/Wine" + algs[a] + "Tests.log"
    args['a'] = a
    var_a = None
    var_b = None
    var_c = None
    loop_a = None
    loop_b = None
    loop_c = None
    if a == 1:
        print("Testing SA")
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if '-temp' in sys.argv[i]:
                    temp = int(sys.argv[i+1])
                elif '-decay' in sys.argv[i]:
                    decay = float(sys.argv[i+1])
            var_a = '-temp'
            var_b = '-decay'
            var_c = ""
            loop_a = range(250,temp, 250)
            loop_b = np.arange(0,decay, 0.05)
            loop_c = range(0,1)
    elif a == 2:
        print("Testing GA")
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if '-popSize' in sys.argv[i]:
                    popSize = int(sys.argv[i+1])
                elif '-toMate' in sys.argv[i]:
                    toMate = int(sys.argv[i+1])
                elif '-toMutate' in sys.argv[i]:
                    toMutate = int(sys.argv[i+1])
            var_a = '-popSize'
            var_b = '-toMate'
            var_c = '-toMutate'
            loop_a = range(toMate, popSize, 100)
            loop_b = range(100, toMate, 100)
            loop_c = range(5, toMutate+1, 5)
                
    elif a == 3:
        print("Testing MIMIC")
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if '-samples' in sys.argv[i]:
                    samples = int(sys.argv[i+1])
                elif '-toKeep' in sys.argv[i]:
                    toKeep = int(sys.argv[i+1])
            var_a = '-samples'
            var_b = '-toKeep'
            var_c = ""
            loop_a = range(toKeep, samples)
            loop_b = range(0, toKeep, 5)

    if var_c:
        data = {var_a: [], var_b: [], var_c: [], 'time': [], 'score': []}
    else:
        data = {var_a: [], var_b: [], 'time': [], 'score': []}

    for i in loop_a:
        for j in loop_b:
            for k in loop_c:
                print(str(i) + "\t" + str(j) + "\t" + str(k))
                data[var_a].append(i)
                data[var_b].append(j)
                time1 = time.time()
                if var_c:
                    data[var_c].append(k)
                    proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.WineTest -a " + str(a) + 
                                            " " + var_a + " " + str(i) + " " + var_b + " " + str(j) + 
                                            " " + var_c + " " + str(k),
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                else:
                    proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.WineTest -a " + str(a) + 
                                            " " + var_a + " " + str(i) + " " + var_b + " " + str(j),
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = proc.communicate()
                time2 = time.time()
                data['time'].append((time2-time1) * 1000.0)
                data['score'].append(float(out.strip()))
    
elif maxIters:
    data = {'a': [], 'iters': [], 'time': [], 'train_err': [], 'test_err': []}
    file_name = "logs/WineIterations.log"
    for a in range(0,4):
        # if a > 1:
        #     rng = range(1, min(maxIters, 20), 1)
        # else:
        rng = range(1, maxIters, step)
        for i in rng:
            print(algs[a] + "\t" + str(i))
            data['a'].append(algs[a])
            data['iters'].append(i)
            time1 = time.time()
            proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.WineTest -i " + str(i) + " -a " + str(a),
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            time2 = time.time()
            out = out.strip().split(', ')
            data['train_err'].append(float(out[0]) / 100)
            data['test_err'].append(float(out[1]) / 100)
            data['time'].append((time2-time1) * 1000.0)
    

df = pd.DataFrame(data)

print(df.head())

df.to_csv(file_name, index=False)