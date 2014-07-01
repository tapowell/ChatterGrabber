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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro19Score.txt"
index = 19
gen = 0
prefix = ''
mode = ["decision tree"]
mode = ["naive bayes"]
SVMMode = 'ratio'
degrees.append(7)
degrees.append(7)
degrees.append(1)
degrees.append(5)
None
None
SVMMode = 'number'
SVMNumber = int(3000*2*0.1*0.1)
mode = ["naive bayes"]
None
None
None
degrees.append(3)
mode = ["decision tree"]
SVMNumber = int(3000*4*0.7*0.7)
SVMNumber = int(3000*4*0.3*0.3)
mode = ["svm"]

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

