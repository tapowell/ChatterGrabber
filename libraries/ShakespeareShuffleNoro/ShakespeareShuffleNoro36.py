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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro36Score.txt"
index = 36
gen = 0
prefix = ''
SVMMode = 'all'
degrees.append(5)
None
mode = ["decision tree"]
SVMMode = 'ratio'
degrees.append(1)
None
SVMMode = 'all'
None
degrees.append(7)
SVMNumber = int(3000*2*0.4*0.4)
degrees.append(7)
None
degrees.append(2)
None
SVMMode = 'number'
None
SVMNumber = int(3000*1*0.6*0.6)
None
degrees.append(2)

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

