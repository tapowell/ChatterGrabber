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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro34Score.txt"
index = 34
gen = 0
prefix = ''
None
SVMNumber = int(3000*3*0.2*0.2)
degrees.append(2)
degrees.append(1)
mode = ["decision tree"]
degrees.append(1)
SVMMode = 'number'
mode = ["max ent"]
None
degrees.append(3)
mode = ["naive bayes"]
SVMMode = 'all'
SVMNumber = int(3000*3*0.4*0.4)
SVMNumber = int(3000*5*0.1*0.1)
degrees.append(6)
SVMNumber = int(3000*7*0.2*0.2)
SVMNumber = int(3000*7*0.2*0.2)
degrees.append(1)
mode = ["naive bayes"]
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
