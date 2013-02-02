#!/usr/bin/python
#KillingJenny 1.62
#A fun killbot for phenny
#by maddux, 2012

from __future__ import division
import random
import os
import time
katiereq = False
armed = False
globalcount = 150
killchance = 50.0
killmod = 23.0
KILLCHAN = "#kill"
SERVICENICK = ["Boxxy"]
BOTNICK = "jenny"
OPERNICK = ""
OPERPASS = ''
EXCEMPTLIST = ['Anonymous9', 'Boxxy', 'katie', 'Eto', BOTNICK, SERVICENICK]


def arm(phenny, input):
	if not input.admin: return
	phenny.write(['oper',OPERNICK,OPERPASS])
	phenny.write(['mode',BOTNICK,'+H'])
	global armed
	armed = True
	phenny.say('Pheer. '+BOTNICK+' haz o:line!')
	phenny.write(['LUSERS'])
arm.commands = ['arm']
arm.priority = 'high'

def disarm(phenny, input):
	if not input.admin: return
	phenny.write(['mode',BOTNICK,'-o'])
	phenny.say('I am disarmed :/')
	global armed
	armed = False
disarm.commands = ['disarm']
disarm.priority = 'high'

def setmod(phenny, input):
	if not input.admin: return
	global killmod
	killmodo = killmod
	killmod = float(input.group(2))
	phenny.say('kill modifier changed from '+str(killmodo)+' to '+str(killmod))
setmod.commands = ['setmod']

def getmod(phenny, input):
	#if not input.admin: return
	global killmod
	phenny.say('kill modifier is currently set to '+str(killmod))
getmod.commands = ['getmod']

def astatus(phenny, input):
	global armed
	if armed == True: phenny.say('I am armed.')
	else: phenny.say('I am disarmed.')
astatus.commands = ['status']

def dokill(phenny, input):
	global killquit
	global killmod
	global globalcount
	global killchance
	for name in EXCEMPTLIST:
		if name == input.nick: return
	if input.admin: 
		phenny.say('d\'aww, I would never /kill you, '+input.nick+'!')
		return
	random.seed()
	#killchance = killmod/globalcount
	phenny.say('Ohai, '+input.nick+'! Let\'s roll the dice of destiny. With a current killing chance of '+str(100*(1-killchance))+'%, you will need a result less than '+str(killchance)+'. Rolling...')
	time.sleep(1)
	randn = random.uniform(0.0,1.0)
	if randn > killchance:
		killquit = True
		phenny.say('Nope. Your result: '+str(randn)+'. Die well :-)')
		phenny.write(['kill',input.nick,'You lost the #kill game (Killing chance: '+str(100*(1-killchance))+'%)'])
		phenny.write(['LUSERS'])
	else:
		phenny.say(str(randn)+' rolled!')
		phenny.say('Yay, you won the #kill game. Welcome to the channel!')
		phenny.write(['mode','#kill','+v',input.nick])
		with open ('killscore.txt','r') as f:
			oldhs = f.readline()
			oldname = f.readline()
			olddate = f.readline()
		ohs = float(oldhs)
		if 100*(1-killchance) > ohs:
			phenny.say('\002NEW HIGHSCORE!\002 Old Highscore: '+oldhs+' by '+oldname+' ('+olddate+')')
			msg = 'Survived joining #kill with a killing chance of '+str(100*(1-killchance))+'% (All-Time Highscore!)'
			phenny.write(['SWHOIS', input.nick, msg])
			hstime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			hsval = str(100*(1-killchance))
			with open ('killscore.txt','w') as f:
				f.write(hsval+'\n')
				f.write(input.nick+'\n')
				f.write(hstime+'\n')
			msg = input.nick+' set a new highscore for #kill!: '+str(100*(1-killchance))+'%. Check if you can reach a new higscore by typing .killstatus in a channel with katie.'
			phenny.write(['WALLOPS',msg])
		else:
			msg = 'Survived joining #kill with a killing chance of '+str(100*(1-killchance))+'%'
			phenny.write(['SWHOIS', input.nick, msg])
		phenny.say('Awarded SWHOIS title. Congratulations, '+input.nick)
		phenny.write(['LUSERS'])
dokill.event = 'JOIN'
dokill.rule = r'.*'
dokill.priority = 'high'

def updatecount(phenny, input):
	phenny.write(['LUSERS'])
updatecount.commands = ['update']

def getcount(phenny, input):
	global killchance
	global globalcount
	global killmod
	global katiereq
	line = input.group().split()
	globalcount = int(line[3])
	killchance = killmod/globalcount
	if katiereq == True: 
		phenny.write(['privmsg','#kill','Update request from katie:'])
		katiereq = False
	msg = 'Current chance of being killed: '+str(100*(1-killchance))+'%'
	phenny.write(['privmsg','#kill',msg])
	with open ('killscore.txt','r') as f:
		hsval  = f.readline()
		hsname = f.readline()
		hstime = f.readline()
	msg = 'All-Time Highscore: '+hsval+'%, set by '+hsname+' ('+hstime+')'
	phenny.write(['privmsg','#kill',msg])
	if 100*(1-killchance) > float(hsval):
		msg = 'Danger, danger! A new higscore is possible on next join!'
		phenny.write(['privmsg','#kill',msg])
	else:
		msg = 'Current Highscore is safe.'
		phenny.write(['privmsg','#kill',msg])
getcount.event = "266"
getcount.rule = r'.*'

def katie_inq(phenny, input):
	if input.nick != 'katie': return
	global katiereq
	katiereq = True
	phenny.write(['LUSERS'])
	time.sleep(1)
	killchance = killmod/globalcount
	phenny.reply(str(100*(1-killchance)))
katie_inq.event = 'PRIVMSG'
katie_inq.rule = r'.*'
