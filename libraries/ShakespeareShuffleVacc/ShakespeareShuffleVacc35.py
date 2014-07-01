from sys import path
from os import getcwd
parent = '/'.join(getcwd().split('/')[:])
print parent
#parent = '..'
if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['vaccAutNLPScores.csv']
cores = 2
iterations = 3
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
stops = 0
fileName = "ShakespeareShuffleVacc/ShakespeareShuffleVacc35Score.txt"
index = 35
gen = 0
prefix = ''
SVMNumber = int(3000*7*0.7*0.7)
SVMMode = 'number'
SVMMode = 'ratio'
mode = ["decision tree"]
SVMNumber = int(3000*6*0.9*0.9)
None
SVMNumber = int(3000*5*0.4*0.4)
degrees.append(4)
None
None
mode = ["naive bayes"]
mode = ["max ent"]
degrees.append(1)
mode = ["naive bayes"]
SVMMode = 'number'
SVMNumber = int(3000*1*0.6*0.6)
degrees.append(4)
SVMMode = 'all'
mode = ["max ent"]
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
