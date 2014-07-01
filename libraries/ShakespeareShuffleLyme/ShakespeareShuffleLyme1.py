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



fileName = "ShakespeareShuffleLyme/ShakespeareShuffleLyme1Score.txt"
index = 1
gen = 0

SVMNumber = int(3000*3*0.1*0.1)
degrees.append(7)
NLPFreqLimit.append(3)
mode = ["svm"]
degrees.append(3)
NLPFreqLimit.append(2)
degrees.append(2)
SVMNumber = int(3000*5*0.5*0.5)
NLPFreqLimit.append(3)
SVMMode = 'ratio'
mode = ["svm"]
NLPFreqLimit.append(3)
SVMMode = 'number'
SVMNumber = int(3000*5*0.3*0.3)
degrees.append(2)
NLPFreqLimit.append(2)
mode = ["decision tree"]
mode = ["max ent"]
degrees.append(6)
NLPFreqLimit.append(3)

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



