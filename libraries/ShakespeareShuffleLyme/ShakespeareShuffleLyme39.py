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



fileName = "ShakespeareShuffleLyme/ShakespeareShuffleLyme39Score.txt"
index = 39
gen = 0

mode = ["decision tree"]
degrees.append(3)
NLPFreqLimit.append(3)
mode = ["naive bayes"]
SVMMode = 'number'
degrees.append(7)
NLPFreqLimit.append(3)
SVMNumber = int(3000*6*0.3*0.3)
SVMMode = 'ratio'
NLPFreqLimit.append(2)
SVMMode = 'ratio'
SVMNumber = int(3000*6*0.5*0.5)
NLPFreqLimit.append(1)
degrees.append(3)
SVMNumber = int(3000*4*0.9*0.9)
SVMNumber = int(3000*5*0.7*0.7)
degrees.append(1)
SVMNumber = int(3000*7*0.6*0.6)
NLPFreqLimit.append(2)
SVMMode = 'all'

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



