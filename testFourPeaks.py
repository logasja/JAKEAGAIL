import os
import sys
import subprocess
import pandas as pd
import time

algs = ['RHC', 'SA', 'GA', 'MIMIC']

args = {}
maxN = 10
maxIters = 0
step = 1

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if '-maxN' in sys.argv[i]:
            maxN = int(sys.argv[i+1])
        elif '-iters' in sys.argv[i]:
            maxIters = int(sys.argv[i+1])
        elif '-step' in sys.argv[i]:
            step = int(sys.argv[i+1])
else:
    exit()

file_name = ""

if not maxIters:
    data = {'a': [], 'N': [], 't': [], 'time': [], 'score': []}
    file_name = "logs/FourPeaksExhaustive.log"
    for a in range(0, 4):
        for N in range(10, maxN+1, 10):
            for t in range(0, N, 5):
                print(str(a) + '\t' + str(N) + '\t' + str(t))
                data['a'].append(algs[a])
                data['N'].append(N)
                data['t'].append(t)
                time1 = time.time()
                proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.FourPeaksTest -a " + str(a) + 
                                        " -t " + str(t) + " -N " + str(N),
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = proc.communicate()
                time2 = time.time()
                data['time'].append((time2-time1) * 1000.0)
                data['score'].append(float(out.strip()))
else:
    data = {'a': [], 'iters': [], 'time': [], 'score': []}
    file_name = "logs/FourPeaksIterations.log"
    for a in range(0,4):
        for i in range(1, maxIters, step):
            data['a'].append(algs[a])
            data['iters'].append(i)
            time1 = time.time()
            proc = subprocess.Popen("java -cp ABAGAIL.jar opt.test.FourPeaksTest -i " + str(i) + " -a " + str(a),
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = proc.communicate()
            time2 = time.time()
            data['time'].append((time2-time1) * 1000.0)
            data['score'].append(float(out.strip()))
    

df = pd.DataFrame(data)

print(df.head())

df.to_csv(file_name, index=False)
