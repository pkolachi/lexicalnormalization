import os

for lang in os.listdir('data'):
    trainFile = 'data/' + lang + '/train.norm'
    devFile = 'data/' + lang + '/dev.norm'
    cmd = 'python3 scripts/baseline.py --method mfr --train ' + trainFile
    if os.path.isfile(devFile):
        cmd += ' --dev ' + devFile
        cmd += ' --out data/' + lang + '/dev.pred'
    else:
        cmd += ' --out data/' + lang + '/train.pred'
    cmd += ' > data/' + lang + '/score'
    print(cmd)
    #os.system(cmd)
