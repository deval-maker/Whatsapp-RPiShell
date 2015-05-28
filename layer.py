# -*- coding: utf-8 -*-
import os, subprocess, time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from yowsup.layers                                     import YowLayer
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

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
		print("Received %s from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
		bdy= str(messageProtocolEntity.getBody())	
		if ('$' in bdy):
			command=bdy.split('$')[1]
			print (bdy + '  received: Shell Mode Activated.' )
			answer='Shell Mode Activated. '
			os.system(command)
			self.toLower(receipt)
			self.toLower(TextMessageProtocolEntity(answer,to = messageProtocolEntity.getFrom()))
		
		else:
			if 'hi' in bdy.lower():
				answer = 'Hello!'
				self.toLower(receipt)	
				self.toLower(TextMessageProtocolEntity(answer, to = messageProtocolEntity.getFrom()))
			else:
				self.toLower(receipt)
				self.toLower(TextMessageProtocolEntity(messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom()))

