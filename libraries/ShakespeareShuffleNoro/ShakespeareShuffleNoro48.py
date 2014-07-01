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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro48Score.txt"
index = 48
gen = 0
prefix = ''
degrees.append(1)
SVMMode = 'number'
mode = ["decision tree"]
SVMNumber = int(3000*6*0.1*0.1)
SVMNumber = int(3000*3*0.4*0.4)
None
SVMNumber = int(3000*5*0.5*0.5)
None
None
SVMMode = 'all'
SVMNumber = int(3000*3*0.2*0.2)
mode = ["max ent"]
SVMMode = 'ratio'
mode = ["naive bayes"]
SVMMode = 'ratio'
degrees.append(2)
mode = ["naive bayes"]
degrees.append(5)
SVMNumber = int(3000*3*0.8*0.8)
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
