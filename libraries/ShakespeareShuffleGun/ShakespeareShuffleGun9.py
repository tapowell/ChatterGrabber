from sys import path
from os import getcwd
parent = '/'.join(getcwd().split('/')[:])
print parent
#parent = '..'
if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['GunTrackerNLTK.csv']
cores = 1
iterations = 1
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
stops = 0
fileName = "ShakespeareShuffleGun/ShakespeareShuffleGun9Score.txt"
index = 9
gen = 0
prefix = ''
degrees.append(6)
SVMNumber = int(3000*5*0.3*0.3)
SVMNumber = int(3000*2*0.3*0.3)
SVMMode = 'number'
SVMMode = 'number'
SVMNumber = int(1*1*0.7)
degrees.append(1)
SVMNumber = int(5*5*0.6)
SVMNumber = int(2*2*0.9)
mode = ["naive bayes"]
SVMNumber = int(7*7*0.7)
mode = ["naive bayes"]
SVMNumber = int(3000*1*0.5*0.5)
SVMMode = 'number'
SVMMode = 'all'
SVMNumber = int(4*4*0.3)
SVMNumber = int(6*6*0.7)
SVMNumber = int(3000*2*0.6*0.6)
None
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

