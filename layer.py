# -*- coding: utf-8 -*-
import os, subprocess, time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from yowsup.layers                                     import YowLayer
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

allowedPersons=['919603427665','919925195998']
ap = set(allowedPersons)
 
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
                if messageProtocolEntity.getFrom(False) in ap:
			print("Received %s from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
			bdy= str(messageProtocolEntity.getBody())
			print bdy
			if 'hi' in bdy.lower():
				answer = 'Hello!'
				self.toLower(receipt)	
				self.toLower(TextMessageProtocolEntity(answer, to = messageProtocolEntity.getFrom()))
			else:
				self.toLower(receipt)
                                self.toLower(TextMessageProtocolEntity(messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom()))
                else:
                        answer = 'You arent a valid sender.'
                        self.toLower(receipt)
                        self.toLower(TextMessageProtocolEntity(answer, to = messageProtocolEntity.getFrom()))
