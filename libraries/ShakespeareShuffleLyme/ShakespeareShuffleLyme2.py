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



fileName = "ShakespeareShuffleLyme/ShakespeareShuffleLyme2Score.txt"
index = 2
gen = 0

SVMMode = 'number'
SVMMode = 'number'
NLPFreqLimit.append(3)
NLPFreqLimit.append(1)
degrees.append(7)
mode = ["max ent"]
SVMNumber = int(3000*6*0.5*0.5)
degrees.append(7)
SVMNumber = int(3000*7*0.2*0.2)
NLPFreqLimit.append(4)
SVMNumber = int(3000*4*0.1*0.1)
NLPFreqLimit.append(2)
mode = ["max ent"]
mode = ["decision tree"]
SVMNumber = int(3000*4*0.5*0.5)
SVMMode = 'ratio'
degrees.append(3)
mode = ["max ent"]
NLPFreqLimit.append(2)
SVMNumber = int(3000*5*0.8*0.8)

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



