# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import tweepy
import datetime, time
import ujson as json
#import json
import os
import tempfile
import subprocess

from random import randint, uniform, choice
from GISpy import *
from KwikECache import updateCache

def setLastRan(self,pad=0):
    pid = os.getpid()
    procName = "TwitterSpout_%s" % pid
    strTime = str(int(time.time())+pad)
    if not os.path.exists('lastRan'):
        os.makedirs('lastRan')
    fileOut = open("lastRan/%s" % procName,'w')
    fileOut.write(strTime)
    fileOut.close()


class giSeeker():
    def __init__(self, conditions, qualifiers, exclusions, api, cfg, name, testSpace, geoCache, NLPClassifier):
        self.delay = 30
        self.qualifiers = qualifiers
        self.conditions = conditions
        self.api = api
        self.name = name
        self.exclusions = exclusions
        self.cfg = cfg
        self.searchDelay = 600
        self.rateLimit = 180
        self.rateIncrement = 900
        self.geoCache = geoCache
        self.useNLP = False
        self.NLP = NLPClassifier
        self.extra = ''
        self.sendStatus = 'sent'
        
        if cfg['OnlyKeepNLP'] != False:
            global TweetMatch
            import TweetMatch
            self.useNLP = True
            temp = cfg['OnlyKeepNLP']
            if type(temp) is str:
                if '_' in temp:
                    self.cfg['OnlyKeepNLP'] = temp.split('_')
                else:
                    self.cfg['OnlyKeepNLP'] = temp.split(' ')
            if type(temp) is list:
                self.cfg['OnlyKeepNLP'] = temp
	    if type(self.cfg['OnlyKeepNLP']) is not list:
		self.cfg['OnlyKeepNLP'] = [str(temp)]
            self.cfg['OnlyKeepNLP'] = [str(key) for key in self.cfg['OnlyKeepNLP']]


	if type(api) is dict:
            print "Using multiple API login method"
            self.multiAPI = True
        else:
            print "Using single API login method"
            self.multiAPI = False

        giSeeker.flushTweets(self)
        giSeeker.makeQueries(self)
        
        if not self.cfg['RegionSearch']:
		geoTemp = getGeo(cfg)
        else:
		geoTemp = "REGION"

        self.pathOut = 'studies/'+self.cfg['OutDir']+'search/'
        if not os.path.exists(self.pathOut):
            os.makedirs(self.pathOut) 
        fileOut = openWhenReady(self.pathOut + 'checkbits','w')
        fileOut.write('DayFinished = False')
        fileOut.close()
            
        giSeeker.getLastID(self)
            
        if geoTemp == "STACK":
            cfg['UseStacking'] = True
            self.geo = "STACK"
	elif geoTemp == 'REGION':
	    self.geo = 'REGION'
        else:
            self.geo = geoString(getGeo(cfg))
            
        if cfg['UseGDI']:
            self.searchDelay = cfg['GDI']['Frequency']
        if cfg['UseStacking']:
            temp = fillBox(cfg,self)
            self.stackPoints = temp['list']
            self.stackRadius = temp['radius']
            self.stackQueries = len(self.queries) * len(self.stackPoints)
            self.stackLastTweet = [[self.lastTweet for _ in xrange(len(self.stackPoints))] for __ in xrange(len(self.queries))]
            self.stackLast = time.time()
                
        self.testSpace = testSpace
        self.runDay = datetime.datetime.now().strftime("%A %d")
        self.lastWrite = 'null'
        self.startDay = 'null'
        

        print "\nInitiated seeker '%s' with %s conditions, %s qualifiers, and %s exclusions" % (name, len(conditions), len(qualifiers), len(exclusions))
            

    
    
    def closeDay(self):
	setLastRan(self,pad=1800)
        print "Closing tweet collection for", self.startDay, '\n'
        fileOut = openWhenReady(self.pathOut + 'checkbits','w')
        directory = self.cfg['Directory']
        fileOut = open(self.pathOut + 'checkbits','w')
        fileOut.write('DayFinished = True') 
        if not self.cfg['UseGDI']:
            try:
                fileOut.write('ConditionsVersion = ' + time.ctime(os.stat(directory + '/lists/' + self.cfg['Conditions']).st_mtime))
                fileOut.write('QualifiersVersion = ' + time.ctime(os.stat(directory + '/lists/' + self.cfg['Qualifiers']).st_mtime))
                fileOut.write('ExclusionsVersion = ' + time.ctime(os.stat(directory + '/lists/' + self.cfg['Exclusions']).st_mtime))
            except:
                fileOut.write('ConditionsVersion = ' + time.ctime(os.stat(directory + self.cfg['Conditions']).st_mtime))
                fileOut.write('QualifiersVersion = ' + time.ctime(os.stat(directory + self.cfg['Qualifiers']).st_mtime))
                fileOut.write('ExclusionsVersion = ' + time.ctime(os.stat(directory + self.cfg['Exclusions']).st_mtime))
        fileOut.close()
        
        
        if self.runDay != datetime.datetime.now().strftime("%A %d"):
            print "End of day noted, updating word banks & reformating past filtered output"
            self.runDay = datetime.datetime.now().strftime("%A %d")
            
            tempQueries = self.queries
            
            if self.cfg['UseGDI']:
                temp = giSpyGDILoad(self.cfg['GDI']['URL'],self.cfg['Directory'])
                lists = temp['lists']
                
                
                for key in temp['config'].keys():
                    self.cfg[key] = temp['config'][key]
                
                geoTemp = getGeo(self.cfg)
            	
		if geoTemp == "STACK":
            	    self.cfg['UseStacking'] = True
            	    self.geo = "STACK"
		elif geoTemp == 'REGION':
	    	    self.geo = 'REGION'
        	else:
            	    self.geo = geoString(getGeo(self.cfg))
                
                logins = temp['login']
                if type(logins) is list:
                    login = getLogins(directory,logins)
       	            self.cfg['MultiLogin'] = True
                else:
                    login = getLogins(directory,[logins])[logins]
                if self.cfg['MultiLogin']:
                    for key in login.keys():
                        temp2 = getAuth(login[key])
                        login[key]['auth'] = temp2['auth']
                        login[key]['api'] = temp2['api']
                        time.sleep(3)
                else:
                    temp2 = getAuth(login)
                    login['auth'] = temp2['auth']
                    login['api'] = temp2['api']
                    login['name'] = self.cfg['userLogin']
                
                self.cfg['_login_'] = login
                
                self.cfg['Directory'] = directory
                #reformatOld(directory, lists, self.cfg, self.geoCache,self.NLP)
                
                tillSend =  datetime.datetime.now().day % int(self.cfg['SendEvery'])
                self.sendStatus = 'sent'
                if tillSend == 0:
                    print "Sending results to GDI user"
                    if True:
                        subprocess.Popen(['python','TwitterSpout.py',self.cfg['GDI']['URL'],'-e'])
                        #sendCSV(self.cfg,directory,self.extra)
                        if self.cfg['AutoUpdate']:
                            os.system('git pull')
                            quit()
                            
                    else:
                    #except Exception as e:
                        print "Unable to send email"
                        print e
                else:
                    print "Sending next report in", tillSend, "days"  
                self.sendStatus = 'sent'
                
            else:
                lists = updateWordBanks(directory, self.cfg)
                reformatOld(directory, lists, self.cfg, self.geoCache,self.NLP)
                self.cfg = getConfig(directory+self.cfg['ConfigFile'])
                
            if self.cfg['UseStacking']:
                temp = fillBox(self.cfg,self)
                tempPoints = self.stackPoints
                
                if tempPoints != temp['list'] or tempQueries != self.queries:
                    self.stackPoints = temp['list']
                    self.stackRadius = temp['radius']
                    self.stackQueries = len(self.stackPoints) * len(self.queries)
                    self.stackLastTweet = [[self.lastTweet for _ in xrange(len(self.stackPoints))] for __ in xrange(len(self.queries))]
                    
                self.stackLast = time.time()
                
            self.conditions = lists['conditions']
            self.qualifiers = lists['qualifiers']
            self.exclusions = lists['exclusions']

    
    def flushTweets(self):
        self.tweetCount = 0
        self.acceptedCount = 0
        self.partialCount = 0
        self.excludedCount = 0
        self.irrelevantCount = 0
        self.jsonRaw = []
        self.jsonAccepted = []
        self.jsonPartial = []
        self.jsonExcluded = []
        self.tweetTypes = {}
        
    
    def saveTweets(self):
        meaningful =  self.jsonAccepted*self.cfg['KeepAccepted'] + self.jsonPartial*self.cfg['KeepPartial'] + self.jsonExcluded*self.cfg['KeepExcluded']
        if len(meaningful)>1:
            print "\nDumping tweets to file, contains %s tweets with %s accepted, %s rejected, %s partial matches, and %s irrelevant" % (len(meaningful),
                        self.acceptedCount,
                        self.excludedCount,
                        self.partialCount,
                        self.irrelevantCount)        
       
            if self.cfg['TweetData'] != 'all':
                meaningful = cleanJson(meaningful,self.cfg,self.tweetTypes)
                
            #timeStamp = datetime.date.today().strftime("%A")
            timeStamp = self.startTime
            self.lastWrite = self.startDay
            
            if self.cfg['KeepRaw']:
                with open(self.pathOut+'Raw_'+self.cfg['FileName']+'_'+timeStamp+'.json', 'w') as outFile:
                    json.dump(self.jsonRaw,outFile)
                outFile.close()
    
            with open(self.pathOut+'FilteredTweets_'+self.cfg['FileName']+'_'+timeStamp+'.json', 'w') as outFile:
                json.dump(meaningful,outFile)
            outFile.close()
            
            print 'Json text dump complete, buffering....'    
            time.sleep(1)
            
            
            giSeeker.flushTweets(self)
        else:
            print "No tweets found for date"
        print "Updating geoPickle"
        self.geoCache = updateGeoPickle(self.geoCache,getPickleName(self.cfg),self.cfg)



    def getLastID(self):
        """Open newest file, finds last ID of tweet recorded"""
        print "\nChecking for last tweet ID loaded..."
        try:
            fileList = os.listdir(self.pathOut)
            fileList = [i for i in fileList if (".json" in i.lower() and i.lower().startswith('raw'))]
            fileList = filter(lambda i: not os.path.isdir(self.pathOut+i), fileList)
            newest = self.pathOut + max(fileList, key=lambda i: os.stat(self.pathOut+i).st_mtime)
            print "\tNewest File:", newest
            inFile = open(newest)
            listed = json.load(inFile)
            jsonToDictFix(listed)
            
            ids = set()
            for tweet in listed:
                ids.add(tweet['id'])
            self.lastTweet = max(ids)
        except:
            print "Unable to find last tweet batch, using ID 0"
            self.lastTweet = 0
        print "\tLast tweet:", self.lastTweet
    
    def reincodeList(self,list,decoder='utf-8',encoder='latin1'):
 	print "DEBOO1",list
	if decoder != 'null':
		list = [entry.decode(decoder) for entry in list]
	if encoder != 'null':
		list = [entry.encode(encoder) for entry in list]
	print "DEBOO2",list
	return list	


    def reincodeTerms(self):
	self.conditions = self.reincodeList(self.conditions)
	self.qualifiers = self.reincodeList(self.qualifiers)
	self.exclusions = self.reincodeList(self.exclusions)
    
    def makeQueries(self):
        """Formats query list and splits into < 1k character segments"""
        self.queries = []

	#self.reincodeTerms()

	if self.conditions != []:
        	text = u'"'+self.conditions[0]+'"'
	else:
		text = u''
        
        for item in self.conditions[1:]:
            entry = u' OR "' + item + u'"'
            if len(text + entry) >= 300:
                
                if not self.cfg['KeepRetweets']:
                    self.queries.append(text + ' -"rt @"')
                else:
                    self.queries.append(text)
                
                text = u'"'+item+'"'
            else:
                text += entry
                
        if not self.cfg['KeepRetweets']:
            self.queries.append(text + ' -"rt @"')
        else:
            self.queries.append(text)

	if self.cfg['RegionSearch']:
		places = []
		fileRef = self.cfg['Directory']+'caches/placeID.pickle'
		placeCache = dict()
		updateCache(placeCache,fileRef,1)
		for place in self.cfg['LocationName']:
		    #print "Pulling location code for", place
		    if self.multiAPI:
			tempApi = self.api[self.api.keys()[0]]['api']
		    else:
			tempApi = self.api
		    done = False
		    while not done:
			try:
				if place in placeCache.keys():
					placeTemp = placeCache[place]
					print "Place id", placeTemp[0].id, "pulled from cache for place", place
				else:
				    if place == 'null':
				        placeCache['place'] = placeTemp = 'null'    
				    else:
		    			placeTemp = tempApi.geo_search(query=place.replace('_',' ').replace('-',' '), granularity=self.cfg['LocationGranularity'])	
					if len(placeTemp) != 0:
						placeCache[place] = placeTemp
						print "Place id", placeTemp[0].id, "found for place", place
						updateCache(placeCache,fileRef,1)
				done = True		
			except Exception,e:
				print "Place lookup for",place,"failed, waiting 2 minutes before retrying"
				print "Error:", e
				time.sleep(120)
		    if len(placeTemp) != 0:
		        if placeTemp == 'null':
		            places.append('null')
		        else:
		    	    places.append(placeTemp[0].id)
		    else:
			print "No place found for", place
		queriesTemp = []
		for query in self.queries:
			for place in places:
			    if place != 'null' and place != '':
				queriesTemp.append('place:%s ' % place + query)
			    else:
			        queriesTemp.append(query)
		self.queries = queriesTemp
            
        for item in self.queries:
	    #print "Deboo",str(item)
            print "Query Length: %s\tContents:\n%s\n" % (len(item),str(item))
                
    def run(self):
        newDay = False
        print "\nPreparing to run..."
        print "Geographic Selection:", self.geo, '\n\n'
        while True:
            collected = []
            foundIDs = set()
            allFound = 0
 
            if self.multiAPI:
		print "Multi-api mode in use"
		failCount = dict([key,0] for key in self.api.keys())
            	APIoffline = dict([key, 0] for key in self.api.keys())

            if self.cfg['UseStacking']:
                    counted = 0; increment = 10
                    timeNow = time.time()
                    elapsed = timeNow - self.stackLast
                    self.stackLast = timeNow
                    stackDelay = getDelay(self, elapsed)
                    print "Running %s geoStack queries at 1 query every %s seconds" % (self.stackQueries,stackDelay)
            
            queryCount = -1
            for query in self.queries:
                #if queryCount % 50 == 0:
                #    setLastRan(self)
                
                if self.cfg['UseStacking']:
                    geoCount = 0; queryCount += 1
                    
                    for geoPoint in self.stackPoints:
                        loggedIn = True
                        ranSearch = False
                        
                        while not loggedIn or not ranSearch:  
                            if geoCount % 20 == 0:
                                setLastRan(self)
                                
                            try:
                                if self.multiAPI:
                                    numOffline = sum((1 for key in APIoffline if APIoffline[key] != 0))
                                    APIoffline = {key:max(value-1,0) for key,value in APIoffline.iteritems()}
				    chooseable = [key for key,value in APIoffline.iteritems() if value == 0]
	
				    if len(chooseable) > 0:
                                        chosen = choice(chooseable)
                                        
				    cellCollected = self.api[chosen]['api'].search(q = query, 
                                                        since_id = self.stackLastTweet[queryCount][geoCount],  
                                                        geocode = geoString(geoPoint),
                                                        result_type="recent",
                                                        count = 100)
                                    failCount[chosen] = 0
				    time.sleep(uniform(0,.05))
                                    
                                else:    
                                    cellCollected = self.api.search(q = query, 
                                                            since_id = self.stackLastTweet[queryCount][geoCount],  
                                                            geocode = geoString(geoPoint),
                                                            result_type="recent",
                                                            count = 100)
                                
                                allFound += len(cellCollected)
				if self.useNLP:
				    if self.cfg['KeepDiscardsNLP']:
				        cellCollected = [status for status in cellCollected if status.id not in foundIDs and (TweetMatch.classifySingle(status.text,self.NLP,self.cfg['NLPnGrams']) in self.cfg['OnlyKeepNLP'] or uniform(0,1)<self.cfg['DiscardSampleNLP'])]
				    else:
                                        cellCollected = [status for status in cellCollected if TweetMatch.classifySingle(status.text,self.NLP,self.cfg['NLPnGrams']) in self.cfg['OnlyKeepNLP'] and status.id not in foundIDs]
                                
                                for cell in cellCollected:
                                    foundIDs.add(cell.id)
                                
                                if len(cellCollected)>0:
                                    collected += cellCollected
                                    self.stackLastTweet[queryCount][geoCount] = int(collected[0].id)
                                    
                                geoCount += 1; counted += 1
                                    
                                ranSearch = True
                                if counted == self.rateLimit/2:
                                    stackDelay = getDelay(self, 0)
                                if counted%increment == 0:
                                    print "Running search %s out of %s with %s hits found and %s ignored" % (counted, self.stackQueries, len(collected), allFound - len(collected))
                                if self.multiAPI:
                                	time.sleep(stackDelay*(float(len(self.api))/max(len(chooseable),1))*0.9)
                                else:
                                	time.sleep(stackDelay)
                            except Exception,e:
                                loggedIn = False
                                while not loggedIn:
                                    if not self.multiAPI:
					print "Experiment", self.cfg['FileName'],"login error, will sleep 120 before reconnection, error code:",e
                                        time.sleep(120 + randint(-3,3))
				    else:
					failCount[chosen] += 1
				    try:
                                        if self.multiAPI:
						if len(chooseable) == 0:
							print "All logins down, will sleep 2 minutes before reconnection, error code:",e
							chosen = [key for key, value in APIoffline.iteritems() if value == min(APIoffline.values())][0]
							time.sleep(120)
							failCount[chosen] = 0
							APIoffline[chosen] = 0
                                        	if failCount[chosen] <= 2:
                                            		self.api[chosen]['api'] = getAuth(self.cfg['_login_'][chosen])['api']
                                            	else:
                                            		APIoffline[chosen] = 100
                                        else:
                                            self.api = getAuth(self.cfg['_login_'])['api']
                                        print "Login successfull"
                                        loggedIn =  True
                                    except Exception,e:
                                        print "Login unsuccessfull\n",e
                                
                else:
                    loggedIn = True
                    ranSearch = False
                    while not loggedIn or not ranSearch:
                        try:
                            #Issue of stream pagination currently unresolved
                            #https://github.com/tweepy/tweepy/pull/296#commitcomment-3404913
                            
                            if self.multiAPI:
                                numOffline = sum((1 for key in APIoffline if APIoffline[key] != 0))
                                APIoffline = {key:max(value-1,0) for key,value in APIoffline.iteritems()}
				chooseable = [key for key,value in APIoffline.iteritems() if value == 0]

				if len(chooseable) > 0:
				    chosen = choice(chooseable)
				    if self.cfg['RegionSearch']:
					cellCollected = self.api[chosen]['api'].search(q = query, 
                                            since_id = self.lastTweet,
                                            result_type="recent",
                                            count = 100)
				    else:
				        cellCollected = self.api[chosen]['api'].search(q = query, 
                                            since_id = self.lastTweet,  
                                            geocode = self.geo,
                                            result_type="recent",
                                            count = 100)
                                failCount[chosen] = 0
				time.sleep(uniform(0,.05))
                                    
                            else:
				if self.cfg['RegionSearch']:
				    cellCollected = self.api.search(q = query, 
                                                        since_id = self.lastTweet,
                                                        result_type="recent",
                                                        count = 100)
				else:
                                    cellCollected = self.api.search(q = query, 
                                                        since_id = self.lastTweet,  
                                                        geocode = self.geo,
                                                        result_type="recent",
                                                        count = 100)
                                                    
                            if self.useNLP:
				    if self.cfg['KeepDiscardsNLP']:
				        cellCollected = [status for status in cellCollected if status.id not in foundIDs and (TweetMatch.classifySingle(status.text,self.NLP,self.cfg['NLPnGrams']) in self.cfg['OnlyKeepNLP'] or uniform(0,1)<self.cfg['DiscardSampleNLP'])]
				    else:
                                        cellCollected = [status for status in cellCollected if TweetMatch.classifySingle(status.text,self.NLP,self.cfg['NLPnGrams']) in self.cfg['OnlyKeepNLP'] and status.id not in foundIDs]                        
                                
                            for cell in cellCollected:
                                foundIDs.add(cell.id)
                                
                            collected += cellCollected    
                                
                            ranSearch = True
                        except Exception,e:
                            loggedIn = False
                            while not loggedIn:
                                    if not self.multiAPI:
					print "Experiment", self.cfg['FileName'],"login error, will sleep 120 before reconnection, error code:",e
                                        time.sleep(120 + randint(-3,3))
				    else:
					failCount[chosen] += 1
				    try:
                                        if self.multiAPI:
						if len(chooseable) == 0:
							print "All logins down, will sleep 2 minutes before reconnection, error code:",e
							chosen = [key for key, value in APIoffline.iteritems() if value == min(APIoffline.values())][0]
							time.sleep(120)
							failCount[chosen] = 0
							APIoffline[chosen] = 0
                                        	if failCount[chosen] <= 2:
                                            		self.api[chosen]['api'] = getAuth(self.cfg['_login_'][chosen])['api']
                                            	else:
                                            		APIoffline[chosen] = 100
                                        else:
                                            self.api = getAuth(self.cfg['_login_'])['api']
                                        print "Login successfull"
                                        loggedIn =  True
                                    except Exception,e:
                                        print "Login unsuccessfull\n",e
                                    
                
            idList = set()            
            inBox = mappable = 0
            
            hasResults = len(collected) != 0

            setLastRan(self)
            
            if hasResults:
                collected = uniqueJson(collected)
                self.startDay = localTime(collected[0].created_at,self.cfg).strftime("%A %d")
                self.startTime = localTime(collected[0].created_at,self.cfg).strftime(timeArgs)
            
            #if self.lastWrite != 'null' and (self.lastWrite != self.startDay):
            if self.runDay != datetime.datetime.now().strftime("%A %d"):
                print "Good morning! New day noted, preparing to save tweets after hour:", self.cfg['SendAfter']
                newDay = True
                self.sendStatus = 'new day'
                
            if datetime.datetime.now().hour >= self.cfg['SendAfter'] and newDay:
                self.sendStatus = 'ready'
                                   
            for status in collected:
                idList.add(int(status.id))
                if (self.startDay != localTime(status.created_at,self.cfg).strftime("%A %d") or self.tweetCount >= self.cfg['StopCount']) and not newDay:
                    giSeeker.saveTweets(self)
                    giSeeker.closeDay(self)
                    self.startDay = localTime(status.created_at,self.cfg).strftime("%A %d")
                    self.startTime = localTime(status.created_at,self.cfg).strftime(timeArgs)
                    
                text = status.text.replace('\n',' ')
                tweetType = checkTweet(self.conditions, self.qualifiers, self.exclusions, text, self.cfg)
                percentFilled = (self.tweetCount*100)/self.cfg['StopCount']
                
                
                geoType = isInBox(self.cfg, self.geoCache, status)
                geoStrictKeep = geoType['inBox'] or not self.cfg['StrictGeoFilter']
                wordStrictKeep = (tweetType != 'excluded' and tweetType != 'retweet') or not self.cfg['StrictWordFilter']
                tweetLocalTime = outTime(localTime(status,self.cfg))
                inBox += geoType['inBox']
                
                loginInfo = "\033[94m%s:%s:%s%%\033[0m" % (self.name,geoType['text'],percentFilled)
                if geoType['inBox'] or self.cfg['KeepUnlocated']:
                    if tweetType == "accepted":
                        tweetPrint = "%s \033[1m%s\t%s\t%s\t%s\033[0m" % (loginInfo,
									text, 
                                    					status.author.screen_name, 
                                 			      	  	tweetLocalTime['full'], 
                        				                status.source)
			print str(tweetPrint)
                        if geoStrictKeep:
                            mappable += 1    
                            self.tweetCount += self.cfg['KeepAccepted']
                            self.acceptedCount += 1
                            self.jsonAccepted.append(status.json)
                    elif tweetType == "excluded":
                        tweetPrint = "%s \033[1m%s\t%s\t%s\t%s\033[0m" % (loginInfo,
                                                                         text,
                                                                         status.author.screen_name,
                                                                         tweetLocalTime['full'],
                                                                         status.source)
                        print str(tweetPrint)

			if geoStrictKeep and wordStrictKeep:
                            self.tweetCount += self.cfg['KeepExcluded']
                            self.excludedCount += 1
                            self.jsonExcluded.append(status.json)
                    elif tweetType == "partial":
			tweetPrint = u"%s %s\t%s\t%s\t%s" % (loginInfo,
			               			    text, 
			                                    status.author.screen_name, 
                                    			    tweetLocalTime['full'], 
                                    			    status.source)
			print str(tweetPrint)
                        if geoStrictKeep:
                            self.tweetCount += self.cfg['KeepPartial']
                            self.partialCount += 1
                            self.jsonPartial.append(status.json)
                    elif tweetType == "retweet":
                        None
                    else:
                        self.irrelevantCount += 1
                if tweetType != "retweet" and self.cfg['KeepRaw'] == True and geoStrictKeep and wordStrictKeep:
                    self.jsonRaw.append(status.json)
                    self.tweetTypes[str(status.id)] = {'tweetType':tweetType,
                        'geoType':geoType['text'],
                        'lat':geoType['lat'],
                        'lon':geoType['lon'],
                        'place':geoType['place'],
                        'fineLocation':geoType['trueLoc'],
                        'day':tweetLocalTime['day'],
                        'time':tweetLocalTime['time'],
                        'date':tweetLocalTime['date']}
                    if self.cfg['OnlyKeepNLP']:
                        self.tweetTypes[str(status.id)]['NLPCat'] = TweetMatch.classifySingle(status.text,self.NLP,self.cfg['NLPnGrams'])
                    
            
            if newDay and self.sendStatus == 'ready':
                giSeeker.saveTweets(self)
                newDay = False
                giSeeker.closeDay(self)
                try:
                    self.startDay = localTime(status.created_at,self.cfg).strftime("%A %d")
                    self.startTime = localTime(status.created_at,self.cfg).strftime(timeArgs)
                except:
                    self.startDay = 'null'
                    self.startTime = 'null'
        
            
            if hasResults:
                self.lastTweet = max(max(list(idList)), self.lastTweet)
                try:
                    tweetsPerHour = float(len(idList)*3600)/((collected[0].created_at-collected[-1].created_at).seconds)
                except:
                    tweetsPerHour = "NA"
            else:
                tweetsPerHour = 0
            print "\nFound %s tweets with %s geolocated and %s mappable hits, will sleep %s seconds until next search" % (len(idList),inBox, mappable,self.searchDelay)
            print "\tInitial day:", self.runDay, "\tCurrent Day:", datetime.datetime.now().strftime("%A %d")
            if hasResults:
                print "\tFirst tweet: %s\tLast tweet: %s\t\tTweets Per Hour: %s" % (collected[0].created_at, collected[-1].created_at, tweetsPerHour)
            time.sleep(self.searchDelay)
            
    
    
    
    
    
    
    
    
    
    
class giListener(tweepy.StreamListener):
    def __init__(self, conditions, qualifiers, exclusions, api, cfg, name, testSpace, geoCache, NLPClassifier):
        self.qualifiers = qualifiers
        self.conditions = conditions
        self.api = api
        self.name = name
        self.exclusions = exclusions
        self.cfg = cfg
        self.testSpace = testSpace
        self.geoCache = geoCache
        giListener.flushTweets(self)
        print "Initiated listener '%s' with %s conditions, %s qualifiers, and %s exclusions" % (name, len(conditions), len(qualifiers), len(exclusions))
        
        self.pathOut = 'studies/'+self.cfg['OutDir']+'stream/'
        if not os.path.exists(self.pathOut):
            os.makedirs(self.pathOut)
            
        fileOut = openWhenReady(self.pathOut + 'checkbits','w')
        fileOut.write('DayFinished = False')
        fileOut.close()
            
    def closeDay(self):
        fileOut = openWhenReady(self.pathOut + 'checkbits','w')
        directory = self.cfg['Directory']
        fileOut = open(self.pathOut + 'checkbits','w')
        fileOut.write('DayFinished = True') 
        fileOut.write('ConditionsVersion = ' + time.ctime(os.stat(directory + self.cfg['Conditions']).st_mtime))
        fileOut.write('QualifiersVersion = ' + time.ctime(os.stat(directory + self.cfg['Qualifiers']).st_mtime))
        fileOut.write('ExclusionsVersion = ' + time.ctime(os.stat(directory + self.cfg['Exclusions']).st_mtime))
        fileOut.close()
        
        lists = updateWordBanks(directory, self.cfg)
        self.conditions = lists['conditions']
        self.qualifiers = lists['qualifiers']
        self.exclusions = lists['exclusions']
        
        
    def flushTweets(self):
        self.tweetCount = 0
        self.acceptedCount = 0
        self.partialCount = 0
        self.excludedCount = 0
        self.irrelevantCount = 0
        self.jsonRaw = []
        self.jsonAccepted = []
        self.jsonPartial = []
        self.jsonExcluded = []
        self.tweetTypes = {}
        self.startTime = localTime(datetime.datetime.now(),self.cfg).strftime(timeArgs)
        self.startDay = localTime(datetime.datetime.today(),self.cfg).strftime("%A")

    
    def saveTweets(self):
        print "\nDumping tweets to file, contains %s tweets with %s accepted, %s rejected, %s partial matches, and %s irrelevant" % (self.cfg['StopCount'],
                        self.acceptedCount,
                        self.excludedCount,
                        self.partialCount,
                        self.irrelevantCount)
        print '\tJson text dump complete....\n'
                
        meaningful =  self.jsonAccepted*self.cfg['KeepAccepted'] + self.jsonPartial*self.cfg['KeepPartial'] + self.jsonExcluded*self.cfg['KeepExcluded']
        
        if self.cfg['TweetData'] != 'all':
            meaningful = cleanJson(meaningful,self.cfg,self.tweetTypes)
            
        timeStamp = self.startTime
        
        if self.cfg['KeepRaw']:
            with open(self.pathOut+'Raw_'+self.cfg['FileName']+'_'+timeStamp+'.json', 'w') as outFile:
                json.dump(self.jsonRaw,outFile)
            outFile.close()

        with open(self.pathOut+'FilteredTweets_'+self.cfg['FileName']+'_'+timeStamp+'.json', 'w') as outFile:
            json.dump(meaningful,outFile)
        outFile.close()
        giListener.flushTweets(self) 
        print "Updating geoPickle"
        self.geoCache = updateGeoPickle(self.geoCache,self.cfg['Directory']+'caches/'+pickleName) 
    
    def on_status(self, status):
        try:
            if self.startDay != localTime(datetime.datetime.today(),self.cfg).strftime("%A") or self.tweetCount >= self.cfg['StopCount']:
                giListener.saveTweets(self)
            text = status.text.replace('\n',' ')
            tweetType = checkTweet(self.conditions, self.qualifiers, self.exclusions, text, self.cfg)
            
            geoType =  isInBox(self.cfg, self.geoCache, status)

            percentFilled = (self.tweetCount*100)/self.cfg['StopCount']
            loginInfo = "\033[94m%s:%s%%\033[0m" % (self.name,percentFilled)
            tweetLocalTime = outTime(localTime(status,self.cfg))
            if geoType['inBox'] or self.cfg['KeepUnlocated']:
                if tweetType == "accepted":
                    print loginInfo, "\033[1m%s\t%s\t%s\t%s\033[0m" % (text, 
                                status.author.screen_name, 
                                tweetLocalTime['full'], 
                                status.source,)
                    self.tweetCount += self.cfg['KeepAccepted']
                    self.acceptedCount += 1
                    self.jsonAccepted.append(status.json)
                elif tweetType == "excluded":
                    print loginInfo, "\033[91m%s\t%s\t%s\t%s\033[0m" % (text, 
                                status.author.screen_name, 
                                tweetLocalTime['full'], 
                                status.source,)
                    self.tweetCount += self.cfg['KeepExcluded']
                    self.excludedCount += 1
                    self.jsonExcluded.append(status.json)
                elif tweetType == "partial":
                    print loginInfo, "%s\t%s\t%s\t%s" % (text, 
                                status.author.screen_name, 
                                tweetLocalTime['full'], 
                                status.source,)
                    self.tweetCount += self.cfg['KeepPartial']
                    self.partialCount += 1
                    self.jsonPartial.append(status.json)
                elif tweetType == "retweet":
                    None
                else:
                    self.irrelevantCount += 1
            if tweetType != "retweet" and self.cfg['KeepRaw'] == True:
                self.jsonRaw.append(status.json)
                self.tweetTypes[str(status.id)] = {'tweetType':tweetType,
                        'geoType':geoType['text'],
                        'lat':geoType['lat'],
                        'lon':geoType['lon'],
                        'place':geoType['place'],
                        'fineLocation':geoType['trueLoc'],
                        'day':tweetLocalTime['day'],
                        'time':tweetLocalTime['time'],
                        'date':tweetLocalTime['date']} 
                if self.cfg['OnlyKeepNLP']:
                    self.tweetTypes[str(status.id)]['NLPCat'] = TweetMatch.classifySingle(status.text,self.NLP)            
                
        except Exception, e:
            print "Encountered exception:", e
            pass
        except KeyboardInterrupt:
            print "Got keyboard interrupt"

    def on_error(self, status_code):
        print "\033[91m***Stream '%s' encountered error with status code %s***\033[0m" % (self.name,status_code)
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True
