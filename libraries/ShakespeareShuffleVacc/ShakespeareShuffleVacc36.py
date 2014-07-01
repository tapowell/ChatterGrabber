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
fileName = "ShakespeareShuffleVacc/ShakespeareShuffleVacc36Score.txt"
index = 36
gen = 0
prefix = ''
mode = ["svm"]
mode = ["decision tree"]
None
None
degrees.append(1)
mode = ["naive bayes"]
SVMNumber = int(3000*7*0.3*0.3)
mode = ["max ent"]
SVMNumber = int(3000*5*0.99*0.99)
SVMNumber = int(3000*6*0.3*0.3)
degrees.append(6)
degrees.append(2)
degrees.append(2)
SVMNumber = int(3000*1*0.6*0.6)
degrees.append(4)
None
SVMNumber = int(3000*6*0.2*0.2)
SVMMode = 'number'
degrees.append(6)
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
