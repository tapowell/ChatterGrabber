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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro2Score.txt"
index = 2
gen = 0
prefix = ''
SVMMode = 'all'
SVMNumber = int(3000*4*0.9*0.9)
degrees.append(1)
SVMMode = 'number'
SVMMode = 'all'
degrees.append(5)
SVMNumber = int(3000*1*0.99*0.99)
degrees.append(5)
mode = ["naive bayes"]
degrees.append(2)
None
SVMNumber = int(3000*7*0.4*0.4)
SVMMode = 'all'
SVMNumber = int(3000*1*0.99*0.99)
None
SVMMode = 'ratio'
mode = ["max ent"]
None
mode = ["decision tree"]
None

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
