#!/usr/bin/python
# -*- coding: utf8 -*-

from oauth2client import file, client, tools
import httplib2, base64, sys, json, os, mimetypes
from apiclient import discovery, errors
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET = 'client_secret.json'

def certificate():
	storage = file.Storage('gmail-python-quickstart.json')
	credentials = storage.get()

	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET,scope=SCOPES,redirect_uri='http://localhost')
		auth_uri = flow.step1_get_authorize_url()
		print(auth_uri)
		auth_code=raw_input("-->")
		credentials = flow.step2_exchange(auth_code)
		storage.put(credentials)

	http = httplib2.Http()
	http = credentials.authorize(http)
	service = discovery.build('gmail', 'v1', http=http)
	return service

def query_mail(gmail_service, user, query_mail):
	try:
		query_response = gmail_service.users().messages().list(userId = user, q = query_mail).execute()
		return query_response
	except (errors.HttpError, error):
		#print ('An error occures : ',error)
		return error

def download_files(gmail_service, user, mailId):
	try:
		get_attachmentId = gmail_service.users().messages().get(userId = user, id = mailId , format = 'full').execute()
		for parts in get_attachmentId['payload']['parts']:
			if parts['filename']:
				data = gmail_service.users().messages().attachments().get(userId = user, messageId = mailId, id = parts['body']['attachmentId']).execute()
				output = open(parts['filename'],'w')
				output.write(base64.urlsafe_b64decode(data['data'].encode("utf-8")))
				output.close
				#print (parts['filename'].encode("utf-8")," download done!")
			else :
				#print ("don't have attachment !")
				pass
	except :
		#print ('An error occures : ',error)
		#return error
		pass

def send_message(gmail_service, user, message):
	try:
		send_mail = gmail_service.users().messages().send(userId = user, body = message).execute()
		print ("Message Id : ",send_mail['id'])
		return send_mail
	except:
		pass

def CreateMessage(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.b64encode(message.as_string())}

if __name__ == '__main__':

	try:
		service = certificate()
		user_profile_response = service.users().getProfile(userId='me').execute()
		print ('messagesTotal:'+str(user_profile_response["messagesTotal"]))
		mail = CreateMessage("purpledoor4921@gmail.com","purpledoor4921@gmail.com","test case","test")
		send_message(service,'me',mail)
		"""
		query_subject = raw_input("subject : ")
		query_result = query_mail(service, 'me', "subject:"+query_subject)
		for mail_id in query_result['messages']:
			#print('mail id : '+str(mail_id['id']))
			download_files(service, 'me', mail_id['id'])
		"""
	except :
		#print('An error occured :',error)
		pass