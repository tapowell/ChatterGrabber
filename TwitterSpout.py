import sys, os
sys.path.insert(0, 'libraries')

import ujson
import tweepy
import time
import random
import TweetMatch

from GISpy import *
from giListener import *
from dateutil import parser

#from multiprocessing import Process, Queue

expected = ['Lat1','Lat2','Lon1','Lon2','Logins','Conditions','Qualifiers','Exclusions']


@classmethod
def parse(cls, api, raw):
    """#Hacky patch for raw json access, not granted in newest tweepy version
        #Method: http://willsimm.co.uk/saving-tweepy-output-to-mongodb/"""
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
   
   
   
def stripWords(text):
    """Filters out non alphanumeric characters, leaves hashtags"""
    listed = ''.join((c if (c.isalnum()) else ' ') for c in text).split()
    return listed
    


def postTweet(api,text,image):
    """Posts a tweet"""
    if image != None and image != 'null':
        api.update_status(text)
        print "posted tweet:", text
        

                                                      
def getTweets(login, cfg, conditions, qualifiers, exclusions, geoCache, NLPClassifier):
    """selects method of tweet aquisition"""
    if cfg['Method'].lower() == 'stream':
        getViaStream(login, cfg, conditions, qualifiers, exclusions, geoCache, NLPClassifier)
    elif cfg['Method'].lower() == 'search':
        getViaSearch(login, cfg, conditions, qualifiers, exclusions, geoCache, NLPClassifier)
    getViaStream(login, cfg, conditions, qualifiers, exclusions, NLPClassifier)
        
        
        

def getViaSearch(login, cfg, conditions, qualifiers, exclusions, geoCache, NLPClassifier):
    """acquires tweets via search method"""
    print "\nSetting up search(es)"
    filterType = cfg['FilterType'].lower()
    if	cfg['MultiLogin']:
	name = 'multi'
	seeker = giSeeker(conditions,qualifiers,exclusions,login,cfg,name,'null',geoCache, NLPClassifier)
    else:
	name = login['name']
	seeker = giSeeker(conditions,qualifiers,exclusions,login['api'],cfg,name,'null',geoCache, NLPClassifier)
    seeker.run()
        
        
               
def getViaStream(login, cfg, conditions, qualifiers, exclusions, geoCache, NLPClassifier):
    """acquires tweets via geo stream"""
    print "\nSetting up listener(s)"
    name = login['name']
    filterType = cfg['FilterType'].lower()

    ear = giListener(conditions,qualifiers,exclusions,login['api'],cfg,name,'null',geoCache)
    print "Logging in via", name,"credentials file"
        
    print "Starting stream:", name, '\n'
    stream = tweepy.Stream(login['auth'], ear, timeout=30.0)   
    while True:
        try:
            if filterType == "conditions":
                stream.filter(track = conditions)
            elif filterType == "location":
                stream.filter(locations=[cfg['Lon1'],cfg['Lat1'],cfg['Lon2'],cfg['Lat2']])
            break
        except Exception, e:
            delay = 30*random.random()
            print "Filter failed, sleeping", int(delay), "seconds..."
            print e
            time.sleep(delay) 
             


def main():
    usingGDoc = False
    NLPClassifier = 'null'
    keepKeys = 'null'
    extra = dict()
    manualTime = 'null'
    
    skipReformat = '-s' in sys.argv
    quickReformat = '-r' in sys.argv and not skipReformat
    oneTimeDump = '-o' in sys.argv and not skipReformat
    quickSend = '-e' in sys.argv and not skipReformat
    if quickSend:
        quickPos = sys.argv.index('-e')
        if quickPos != len(sys.argv) - 1:
            tArg = sys.argv[quickPos+1]
            try:
                manualTime = parser.parse(tArg)
                print "Sending historic one time report for time %s" % manualTime
            except:
                pass
    
    
    skipReformat = not(quickReformat or oneTimeDump or quickSend) or skipReformat
    
    try: 
        userLogin = sys.argv[2]
        print "Login '%s' passed explicitly" % (userLogin)
    except:
        userLogin = 'null'
    try:
        temp = sys.argv[1]
        if temp.startswith('http'):
            usingGDoc = True
            gDocURL = temp
            print "Preparing GDI Remote Access Loader"
        else:
            print "\nTaking user parameters"
            directory = '/'.join(temp.split('/')[:-1])
            configFile = temp.split('/')[-1]
            if directory == '':
                directory = os.getcwd() + '/'
    except:
        print "Taking default parameters"
        directory = os.getcwd() + '/'
        configFile = 'config'
        
    if usingGDoc:
        directory = os.getcwd() + '/'
        temp = giSpyGDILoad(gDocURL,directory)
        cfg = temp['config']
        lists = temp['lists']
        if type(temp['login']) is list:
            login = getLogins(directory,temp['login'])
	    cfg['MultiLogin'] = True
        else:
            login = getLogins(directory,[temp['login']])[temp['login']]
        cfg['Directory'] = directory
        #geoCache = dict()
        geoCache = updateGeoPickle({},getPickleName(cfg),cfg)
        
        if cfg['OnlyKeepNLP'] != False:
            temp = cfg['OnlyKeepNLP']
            if type(temp) is str:
                cfg['OnlyKeepNLP'] = temp.split('_')
            if type(temp) is list:
                cfg['OnlyKeepNLP'] = temp
	    if type(cfg['OnlyKeepNLP']) is not list:
		cfg['OnlyKeepNLP'] = [str(temp)]
            cfg['OnlyKeepNLP'] = [str(key) for key in cfg['OnlyKeepNLP']]
            NLPClassifier = TweetMatch.getClassifier(cfg['NLPFile'],cfg)
        
        cfg['OneTimeDump'] = oneTimeDump
        cfg['QuickSend'] = quickSend
        if oneTimeDump:
                cfg['DaysBack'] = 'all'
        
        if not skipReformat:
	    reformatOld(directory,lists,cfg,geoCache,NLPClassifier,manualTime=manualTime)
	    geoCache = updateGeoPickle(geoCache,getPickleName(cfg),cfg)
        if quickReformat or oneTimeDump or quickSend:
            quit()        	
        
    else: 
        print "Loading parameters from config file '%s' in directory '%s'" % (configFile, directory)
        cfg = getConfig(directory+configFile)
        cfg['Directory'] = directory
        cfg['ConfigFile'] = configFile
        logins = getLogins(directory, cfg['Logins'])
        lists = updateWordBanks(directory, cfg)
        #geoCache = dict()
        geoCache = updateGeoPickle({},directory+'caches/'+pickleName)
	if not skipReformat:        
		reformatOld(directory,lists,cfg,geoCache,NLPClassifier,manualTime=manualTime) 
		if quickReformat:
			quit()        
		geoCache = updateGeoPickle(geoCache,directory+'caches/'+pickleName)
        
        
        print "\nPlease choose login number:"
        if userLogin == 'null':
            listed = sorted(logins.keys()); i = 0
            for key in listed:
                print "\t%s - %s - %s" % (i,key,logins[key]['description'])
                i += 1
            while True:
                try:
                    selection = int(raw_input('\n:'))
                    userLogin = listed[selection]
                    break
                except:
                    None
 
        login = logins[userLogin]
    
    
    if cfg['MultiLogin']:
        for key in login.keys():
            temp = getAuth(login[key])
            login[key]['auth'] = temp['auth']
            login[key]['api'] = temp['api']
            time.sleep(3)
    else:
        temp = getAuth(login)
        login['auth'] = temp['auth']
        login['api'] = temp['api']
        login['name'] = userLogin
    
    cfg['userLogin'] = userLogin    
    cfg['_login_'] = login
    cfg['Directory'] = directory
    cfg['args'] = sys.argv  
 
    getTweets(login,cfg,lists['conditions'],lists['qualifiers'],lists['exclusions'],geoCache,NLPClassifier)

main()
