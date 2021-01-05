from optparse import OptionParser

def evaluate(raw, gold, pred, ignCaps=False, verbose=False):
    cor = 0
    changed = 0
    total = 0

    if len(gold) != len(pred):
        err('Error: gold normalization contains a different numer of sentences(' + str(len(gold)) + ') compared to system output(' + str(len(pred)) + ')')

    for sentRaw, sentGold, sentPred in zip(raw, gold, pred):
        if len(sentGold) != len(sentPred):
            err('Error: a sentence has a different length in you output, check the order of the sentences')
        for wordRaw, wordGold, wordPred in zip(sentRaw, sentGold, sentPred):
            if ignCaps:
                wordRaw = wordRaw.lower()
                wordGold = wordGold.lower()
                wordPred = wordPred.lower()
            if wordRaw != wordGold:
                changed += 1
            if wordGold == wordPred:
                cor += 1
            elif verbose:
                print(wordRaw, wordGold, wordPred)
            total += 1

    accuracy = cor / total
    lai = (total - changed) / total
    err = (accuracy - lai) / (1-lai)

    print('Baseline acc.(LAI): {:.2f}'.format(lai * 100)) 
    print('Accuracy:           {:.2f}'.format(accuracy * 100)) 
    print('ERR:                {:.2f}'.format(err * 100))

    return lai, accuracy, err

def loadNormData(path):
    rawData = []
    goldData = []
    curSent = []

    for line in open(path):
        tok = line.strip().split('\t')

        if tok == [''] or tok == []:
            rawData.append([x[0] for x in curSent])
            goldData.append([x[1] for x in curSent])
            curSent = []

        else:
            if len(tok) > 2:
                err('erroneous input, line:\n' + line + '\n in file ' + path + ' contains more then two elements')
            if len(tok) == 1:
                tok.append('')
            curSent.append(tok)

    # in case file does not end with newline
    if curSent != []:
        rawData.append([x[0] for x in curSent])
        goldData.append([x[1] for x in curSent])
    return rawData, goldData

def err(msg):
    print('Error: ' + msg)
    exit(0)

if __name__ == '__main__':
    parser = OptionParser(description='Normalization baselines')
    parser.add_option("--gold", help='path to the gold normalization data')
    parser.add_option("--pred", help='path to the system output normalization')
    parser.add_option("--ignCaps", action='store_true', default=False, help='lowercase everything')
    parser.add_option("--verbose", action='store_true',  default=False, help='print the errors made by the system')

    (opts, args) = parser.parse_args()
    if opts.gold == None:
        err('Please provide gold data with --gold')
    if opts.pred == None:
        err('Please provide system output with --pred')
    
    goldRaw, goldNorm = loadNormData(opts.gold)
    predRaw, predNorm = loadNormData(opts.pred)
    evaluate(goldRaw, goldNorm, predNorm, opts.ignCaps, opts.verbose)

