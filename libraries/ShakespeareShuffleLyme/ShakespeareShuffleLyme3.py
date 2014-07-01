from sys import path
from os import getcwd

parent = '/'.join(getcwd().split('/')[:])

if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['lymeScores.csv']
cores = 1
iterations = 1
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
NLPFreqLimit = []
stops = 0
prefix = ''



fileName = "ShakespeareShuffleLyme/ShakespeareShuffleLyme3Score.txt"
index = 3
gen = 0

degrees.append(6)
degrees.append(2)
degrees.append(2)
NLPFreqLimit.append(4)
degrees.append(2)
SVMNumber = int(3000*3*0.1*0.1)
SVMNumber = int(3000*3*0.4*0.4)
SVMNumber = int(3000*2*0.7*0.7)
mode = ["naive bayes"]
SVMMode = 'all'
degrees.append(7)
degrees.append(7)
mode = ["naive bayes"]
SVMMode = 'ratio'
SVMNumber = int(3000*3*0.8*0.8)
degrees.append(7)
SVMMode = 'number'
NLPFreqLimit.append(3)
SVMNumber = int(3000*1*0.6*0.6)
mode = ["max ent"]

outFile = open(fileName,'w')
if degrees == []:
	print "No degrees found, quitting"
	outFile.write('0')
	outFile.close()
	quit()

if mode == "decision tree":
	NLPFreqLimit = [max(2,entry) for entry in NLPFreqLimit]
	degrees = list(set(degrees))[:1]

cfg = {'SVMMode':SVMMode,
	'SVMNumber':SVMNumber,
	'NLPFreqLimit':NLPFreqLimit}
	
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




