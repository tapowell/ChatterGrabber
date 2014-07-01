from sys import path
from os import getcwd
parent = '/'.join(getcwd().split('/')[:])
print parent
#parent = '..'
if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['EmergNLTKScoring.csv']
cores = 1
iterations = 1
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
stops = 0
fileName = "ShakespeareShuffleEmerg/ShakespeareShuffleEmerg48Score.txt"
index = 48
gen = 4
prefix = ''
degrees.append(3)
SVMNumber = int(4*4*0.1)
None
SVMMode = 'all'
degrees.append(4)
None
SVMMode = 'all'
mode = ["naive bayes"]
mode = ["svm"]
None
SVMNumber = int(3000*5*0.4*0.4)
mode = ["naive bayes"]
SVMNumber = int(6*6*0.6)
SVMNumber = int(3000*6*0.7*0.7)
SVMMode = 'ratio'
SVMNumber = int(7*7*0.4)
SVMMode = 'number'
SVMMode = 'ratio'
None
degrees.append(4)

outFile = open(fileName,'w')
cfg = {'SVMMode':SVMMode,
	'SVMNumber':SVMNumber,
	'SVMOrder':'GVTMACFSNN'}
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

