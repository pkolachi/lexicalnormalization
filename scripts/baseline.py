'''
This script provides the baselines for the lexical normalization task, 
which is the translation of social media text to canonical text:
new pix      comming tomoroe
new pictures coming  tomorrow

The script provides two different strategies, Leave-As-Is (LAI) and 
Most-Frequent-Replacement (MFR). 
'''

from optparse import OptionParser
import normEval

def err(msg):
    print('Error: ' + msg)
    exit(0)

def lai(devRaw):
    return devRaw

def mfr(trainRaw, trainGold, devRaw):
    # first count the frequenties of all replacements
    # counts will be a dictionary of words, where each word has a dictionary of counts:
    # counts = {'your': {'you\'re':4, 'your':2}}
    counts = {}
    for sentRaw, sentGold in zip(trainRaw, trainGold):
        for wordRaw, wordGold in zip(sentRaw, sentGold):
            if wordRaw not in counts:
                counts[wordRaw] = {}
            if wordGold not in counts[wordRaw]:
                counts[wordRaw][wordGold] = 0
            counts[wordRaw][wordGold] += 1
    
    # predict the most frequent replacement for each word
    predictions = []
    for sent in devRaw:
        predictions.append([])
        for word in sent:
            if word in counts:
                replacement = max(counts[word], key=counts[word].get)
            else:
                replacement = word
            predictions[-1].append(replacement)
    return predictions

def write(origs, predictions, path):
    outFile = open(path, 'w')
    for origSent, predSent in zip(origs, predictions):
        for origWord, predWord in zip(origSent, predSent):
            outFile.write(origWord + '\t' + predWord + '\n')
        outFile.write('\n')
    outFile.close()

if __name__ == '__main__':
    parser = OptionParser(description='Normalization baselines')
    parser.add_option("--method", default='LAI', help='method to use: \'LAI\' or \'MFR\'')
    parser.add_option("--train", help='path to training data')
    parser.add_option("--dev", help='path to development data, if not specified run k-fold')
    parser.add_option("--kfold", type=int, default=10, help='specify the number of folds to use (when --dev is not given), default=10')
    parser.add_option("--out" , default='', help='path to write normalization to')
    (opts, args) = parser.parse_args()

    if opts.method == None:
        err('please provide --method')
    if opts.method.lower() not in ['lai', 'mfr']:
        err('--method should be one of [\'lai\', \'mfr\']')
    if opts.train == None:
        err('please provide path to train data with --train')

    # K-fold
    if opts.dev == None:
        trainRaw, trainGold = normEval.loadNormData(opts.train)
        predictions = []
        
        splitSize = int(len(trainRaw)/opts.kfold)
        for i in range(opts.kfold):
            beg = i * splitSize
            end = (i+1) * splitSize
            if i == opts.kfold-1: #to ensure we get the whole set
                end = len(trainRaw)

            splitDevRaw = trainRaw[beg:end]
            splitTrainRaw = trainRaw[0:beg] + trainRaw[end:]
            splitTrainGold = trainGold[0:beg] + trainGold[end:]
            
            if opts.method.lower() == 'lai':
                predictions += lai(splitDevRaw)
            else:
                predictions += mfr(splitTrainRaw, splitTrainGold, splitDevRaw)

        if(opts.out != ''):
            write(trainRaw, predictions, opts.out)
        normEval.evaluate(trainRaw, trainGold, predictions)

    # train-dev
    else:
        trainRaw, trainGold = normEval.loadNormData(opts.train)
        devRaw, devGold = normEval.loadNormData(opts.dev)

        if opts.method.lower() == 'lai':
            predictions = lai(devRaw)
        else:
            predictions = mfr(trainRaw, trainGold, devRaw)

        if(opts.out != ''):
            write(devRaw, predictions, opts.out)
        normEval.evaluate(devRaw, devGold, predictions)


