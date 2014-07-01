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
fileName = "ShakespeareShuffleGun/ShakespeareShuffleGun12Score.txt"
index = 12
gen = 0
prefix = ''
SVMMode = 'number'
SVMNumber = int(3000*4*0.8*0.8)
SVMNumber = int(3000*2*0.99*0.99)
None
SVMMode = 'ratio'
SVMMode = 'ratio'
None
SVMNumber = int(3000*4*0.99*0.99)
mode = ["naive bayes"]
SVMNumber = int(3000*4*0.7*0.7)
degrees.append(4)
SVMMode = 'number'
SVMNumber = int(3000*3*0.6*0.6)
SVMMode = 'all'
SVMNumber = int(3000*2*0.4*0.4)
None
mode = ["naive bayes"]
None
SVMNumber = int(3000*3*0.9*0.9)
SVMNumber = int(3000*2*0.8*0.8)

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
