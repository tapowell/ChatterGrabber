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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro45Score.txt"
index = 45
gen = 0
prefix = ''
mode = ["decision tree"]
SVMMode = 'ratio'
SVMMode = 'ratio'
SVMMode = 'ratio'
SVMNumber = int(3000*1*0.7*0.7)
SVMMode = 'all'
SVMMode = 'ratio'
None
SVMMode = 'number'
SVMMode = 'all'
SVMMode = 'all'
None
SVMNumber = int(3000*2*0.8*0.8)
SVMMode = 'all'
SVMMode = 'ratio'
mode = ["naive bayes"]
None
mode = ["svm"]
SVMMode = 'number'
degrees.append(3)

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

