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



fileName = "ShakespeareShuffleLyme/ShakespeareShuffleLyme28Score.txt"
index = 28
gen = 0

SVMMode = 'ratio'
degrees.append(3)
SVMMode = 'ratio'
SVMMode = 'number'
mode = ["naive bayes"]
mode = ["decision tree"]
mode = ["max ent"]
SVMMode = 'number'
SVMMode = 'all'
mode = ["decision tree"]
mode = ["naive bayes"]
mode = ["max ent"]
mode = ["decision tree"]
SVMMode = 'number'
SVMNumber = int(3000*4*0.9*0.9)
mode = ["naive bayes"]
mode = ["svm"]
SVMNumber = int(3000*5*0.4*0.4)
SVMNumber = int(3000*3*0.7*0.7)
degrees.append(5)

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




