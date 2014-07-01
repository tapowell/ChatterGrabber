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
fileName = "ShakespeareShuffleNoro/ShakespeareShuffleNoro16Score.txt"
index = 16
gen = 0
prefix = ''
degrees.append(3)
SVMMode = 'all'
None
degrees.append(3)
degrees.append(1)
SVMMode = 'number'
SVMNumber = int(3000*5*0.4*0.4)
degrees.append(4)
mode = ["decision tree"]
SVMNumber = int(3000*3*0.5*0.5)
SVMNumber = int(3000*6*0.1*0.1)
SVMMode = 'all'
SVMMode = 'number'
SVMNumber = int(3000*2*0.99*0.99)
SVMMode = 'ratio'
SVMMode = 'all'
degrees.append(6)
degrees.append(5)
None
SVMMode = 'ratio'

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

