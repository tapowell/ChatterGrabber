clusterDir = "/home/NDSSL/study/ChatterGrabber/libraries/"
from sys import path
from os import getcwd

parent = clusterDir

if parent not in path:
	path.insert(0, parent)
import optimizeClassifier

files = ['lymeScores.csv']
cores = 5
iterations = 5
sweepRange = [0.9]
degrees =  []
SVMMode = 'number'
SVMNumber = 1000
NLPFreqLimit = []
stops = 0
prefix = ''



fileName = "/home/NDSSL/study/ChatterGrabber/libraries/ShakesLyme/ShakesLyme178Score.txt"
index = 178
gen = 0

NLPFreqLimit.append(5)
NLPFreqLimit.append(4)
SVMNumber = int(3000*5*0.2*0.2)
NLPFreqLimit.append(4)
SVMNumber = int(3000*1*0.3*0.3)
SVMNumber = int(3000*3*0.2*0.2)
SVMMode = 'number'
degrees.append(7)
mode = ["svm"]
degrees.append(1)
mode = ["max ent"]
degrees.append(4)
NLPFreqLimit.append(1)
mode = ["naive bayes"]
NLPFreqLimit.append(3)
SVMMode = 'number'
mode = ["svm"]
degrees.append(6)
mode = ["svm"]
SVMMode = 'all'

outFile = open(fileName,'w')
if degrees == []:
	print "No degrees found, quitting"
	outFile.write('0')
	outFile.close()
	quit()

if ["decision tree"] == mode:
	NLPFreqLimit = [max(2,entry) for entry in NLPFreqLimit]
	degrees = list(set(degrees))[:2]

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
	'files':files,
	'workingDir':clusterDir,
	'cluster':True}

try:
	score = float(optimizeClassifier.main(args,'mendel'))
	outFile.write(str(score))
except:
	outFile.write('0')

outFile.close()




