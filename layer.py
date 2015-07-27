# -*- coding: utf-8 -*-
import os, subprocess, time
import commands
from yowsup.layers                                     import YowLayer
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity


ShellInstanceDictionary = dict()

allowedPersons=['NUMBER_ALLOWED1','NUMBER_ALLOWED2','NUMBER_ALLOWED3','NUMBER_ALLOWED4']
ap = set(allowedPersons)

notAllowedCommands=['nano','reboot','shutdown','killall','kill','rf']
nac = set(notAllowedCommands)

class EchoLayer(YowInterfaceLayer):
	
	@ProtocolEntityCallback("message")
	def onMessage(self, messageProtocolEntity):                                        
		if messageProtocolEntity.getType() == 'text':
			self.onTextMessage(messageProtocolEntity)
   	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery",entity.getFrom())
		self.toLower(ack)
	
	def onTextMessage(self, messageProtocolEntity):
		receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom()) 
		localTime = time.asctime( time.localtime(time.time()) )
		print("Received %s from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
		log = str(messageProtocolEntity.getFrom(False)) + "\t" + localTime  + "\t" + str(messageProtocolEntity.getBody())
		allLogFile= open("all.log","a")
		allLogFile.write(log)
		allLogFile.write("\n")
		allLogFile.close()
		bdy= str(messageProtocolEntity.getBody())	
		bdy = bdy + ' '
		if ('$' in bdy):
			command=bdy.split('$')[1]
			cmdLog = str(messageProtocolEntity.getFrom(False)) + "\t" + localTime  + "\t" + command
			cmdLogFile= open("cmd.log","a")
			cmdLogFile.write(cmdLog)
			cmdLogFile.write("\n")
			cmdLogFile.close()
			if ( (command.split(' ')[0] in nac ) or (command.split(' ')[1] in nac) ):
				print (command + '  unAuthorised Command Given' )
				answer='This command is not authorised for you.'
				self.toLower(receipt)
				self.toLower(TextMessageProtocolEntity(answer,to = messageProtocolEntity.getFrom()))
			else:
				print (command + '  will be executed in shell\n' )
				
				'''
				status,output=commands.getstatusoutput(command)
				opList=output.split("\n")
				opNew=''
				for element in opList:
					opNew += element + '\n'
				if (status != 0):
					answer='There is an error: \n' + opNew
				else:
					answer = opNew
				
				'''
				command = command + '\n'
				phnnumber = str(messageProtocolEntity.getFrom(False))
				print phnnumber

				if (phnnumber in ShellInstanceDictionary):
					shellexist = ShellInstanceDictionary[phnnumber] 
					shellexist.stdin.write(command) 
					answer = shellexist.stdout.readline()
					print answer
					print "number exists"
				else:
					shellnew = subprocess.Popen(['/bin/bash'],shell = False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
					print "shell created"
					ShellInstanceDictionary[phnnumber] = shellnew
					print "dictionary element added"
					shellnew.stdin.write(command)
					print "command sent to shell"
					answer = shellnew.stdout.readline()
					print answer

				print ShellInstanceDictionary

				self.toLower(receipt)
				self.toLower(TextMessageProtocolEntity(answer,to = messageProtocolEntity.getFrom()))
		else:
			if 'ssup' in bdy.lower():
				answer = 'Hello!'
				self.toLower(receipt)	
				self.toLower(TextMessageProtocolEntity(answer, to = messageProtocolEntity.getFrom()))
			else:
				self.toLower(receipt)
				self.toLower(TextMessageProtocolEntity(messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom()))