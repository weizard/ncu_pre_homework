#!/bin/python
# -*- coding: utf-8 -*-

from oauth2client import file, client, tools
import sys
import httplib2
from apiclient import discovery, errors
import json
import base64
import binascii

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET = 'client_secret.json'

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

try:
	user_profile_response = service.users().getProfile(userId='me').execute()
	print ('messagesTotal:'+str(user_profile_response["messagesTotal"]))

	user_mail_response = service.users().messages().get(userId = 'me', id ='151e7cc2cce9a31a', format='full').execute()
	for part in user_mail_response['payload']['parts']:
		
		if part['filename']:
			data = service.users().messages().attachments().get(userId = 'me', messageId ='151e7cc2cce9a31a', id = part['body']['attachmentId'] ).execute()
			print (data['size'])
			
			f = open(part['filename'],'w')
			f.write(base64.urlsafe_b64decode(data['data'].encode("utf-8")))
			f.close()

	query = "subject:研究所指導老師相關事宜詢問"
	user_mail_query_subject_response = service.users().messages().list(userId = 'me', q = query).execute()
	#print (json.dumps(user_mail_query_subject_response))
	for mail_ids in user_mail_query_subject_response['messages']:
		print ('mail id:'+str(mail_ids['id']))
	
except errors.HttpError, error:
	print('An error occured :',error)