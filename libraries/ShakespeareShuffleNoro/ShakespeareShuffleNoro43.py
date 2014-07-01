from sys import path
from os import getcwd
parent = '/'.join(getcwd().split('/')[:])
print parent
#parent = '..'
if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['NLTK_Ready_Tweets.csv']
cores = 2
iterations = 3
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
stops = 0
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro43Score.txt"
index = 43
gen = 0
prefix = ''
None
degrees.append(6)
SVMMode = 'all'
SVMMode = 'ratio'
mode = ["decision tree"]
None
mode = ["naive bayes"]
degrees.append(2)
mode = ["svm"]
None
mode = ["decision tree"]
mode = ["decision tree"]
SVMNumber = int(3000*6*0.7*0.7)
None
mode = ["decision tree"]
SVMMode = 'ratio'
mode = ["svm"]
mode = ["svm"]
mode = ["naive bayes"]
degrees.append(4)

outFile = open(fileName,'w')
cfg = {'SVMMode':SVMMode,
	'SVMNumber':SVMNumber}
args = {'cores':cores,
	'iterations':iterations,
	'sweepRange':sweepRange,
	'degrees':[list(set(degrees))],
	'mode':mode,
	'cfg':cfg,
	'stops':stops,
	'prefix':prefix,
	'files':files}
try:
	score = int(optimizeClassifier.main(args,'mendel'))
	outFile.write(str(score))
except:
	outFile.write('0')

outFile.close()

