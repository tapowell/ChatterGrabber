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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro46Score.txt"
index = 46
gen = 0
prefix = ''
mode = ["decision tree"]
mode = ["decision tree"]
mode = ["decision tree"]
None
mode = ["max ent"]
mode = ["svm"]
SVMNumber = int(3000*3*0.4*0.4)
degrees.append(4)
degrees.append(2)
SVMNumber = int(3000*5*0.6*0.6)
SVMNumber = int(3000*6*0.99*0.99)
None
None
SVMMode = 'all'
SVMMode = 'ratio'
mode = ["decision tree"]
mode = ["max ent"]
SVMMode = 'number'
degrees.append(3)
SVMMode = 'all'

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
