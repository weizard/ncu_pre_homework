#!/usr/bin/python
# -*- coding: utf8 -*-

from oauth2client import file, client, tools
import httplib2, base64, sys, json, os, mimetypes, argparse
from apiclient import discovery, errors
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET = 'client_secret.json'

def certificate():
	storage = file.Storage('gmail-python.json')
	credentials = storage.get()

	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET,scope=SCOPES,redirect_uri='http://localhost')
		flow.user_agent = flow.step1_get_authorize_url()
		parser = argparse.ArgumentParser(parents=[tools.argparser])
		flags = parser.parse_args()
		credentials = tools.run_flow(flow, storage, flags)
		"""
		#by using browser
		flow = client.flow_from_clientsecrets(CLIENT_SECRET,scope=SCOPES,redirect_uri='http://localhost')
		auth_uri = flow.step1_get_authorize_url()
		print('請連接下列網址進行認證，並將回傳的code輸入程式中')
		print(auth_uri)
		auth_code=raw_input("-->")
		credentials = flow.step2_exchange(auth_code)
		"""
		storage.put(credentials)

	http = httplib2.Http()
	http = credentials.authorize(http)
	service = discovery.build('gmail', 'v1', http=http)
	return service

def list_mail(gmail_service, user, max_result ):
	try:
		query_response = gmail_service.users().messages().list(userId = user, maxResults = max_result).execute()
		return query_response
	except (errors.HttpError, error):
		#print ('An error occures : ',error)
		return error

def query_mail(gmail_service, user, query_mail):
	try:
		query_response = gmail_service.users().messages().list(userId = user, q = query_mail, maxResults = 50).execute()
		return query_response
	except (errors.HttpError, error):
		#print ('An error occures : ',error)
		return error

def get_mail_detail(gmail_service, user, mailId):
	try:
		mail_detail = gmail_service.users().messages().get(userId = user, id = mailId , format = 'full').execute()
		return mail_detail
	except:
		pass

def download_files(gmail_service, user, mailId):
	try:
		get_attachmentId = get_mail_detail(gmail_service, user, mailId)
		for parts in get_attachmentId['payload']['parts']:
			if parts['filename']:
				data = gmail_service.users().messages().attachments().get(userId = user, messageId = mailId, id = parts['body']['attachmentId']).execute()
				output = open(parts['filename'],'w')
				output.write(base64.urlsafe_b64decode(data['data'].encode("utf-8")))
				output.close
				print (str(parts['filename'].encode("utf-8"))+" download done!")
				fname = parts['filename']
				#print ('download done !')
				#return fname
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
		#print ("Message Id : ",send_mail['id'])
		print ('mail sended')
		return send_mail
	except errors.HttpError, error:
		#pass
		print error

def create_message(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['To'] = to
	message['From'] = sender
	message['Subject'] = subject
	return {'raw': base64.b64encode(message.as_string())}

def create_message_with_attachment(sender, to, subject, message_text, files_path):
	try:
		message = MIMEMultipart()
		message['To'] = to
		message['From'] = sender
		message['Subject'] = subject

		msg = MIMEText(message_text)
		message.attach(msg)

		for file_path in files_path :
			path = os.path.expanduser(file_path)
			filename = path.split('/')[-1]

			#print (path)
			#print (filename)
			#print os.path.exists(path)
			content_type, encoding = mimetypes.guess_type(path)
			#print (content_type)
			#print (encoding)

			if content_type is None or encoding is not None:
				content_type = 'application/octet-stream'
			main_type, sub_type = content_type.split('/', 1)
			#print main_type
			#print sub_type
			if main_type == 'text':
				fp = open(path, 'rb')
				msg = MIMEText(fp.read(), _subtype=sub_type)
				fp.close()
			elif main_type == 'image':
				fp = open(path, 'rb')
				msg = MIMEImage(fp.read(), _subtype=sub_type)
				fp.close()
			elif main_type == 'audio':
				fp = open(path, 'rb')
				msg = MIMEAudio(fp.read(), _subtype=sub_type)
				fp.close()
			else:
				fp = open(path, 'rb')
				#msg = MIMEBase(main_type, sub_type)
				msg = MIMEBase('application', 'octet-stream')
				msg.set_payload(fp.read())
				fp.close()

			msg.add_header('Content-Disposition', 'attachment', filename=filename)
			message.attach(msg)

		#return {'raw':encoders.encode_base64(message.as_string())}
		return {'raw': base64.urlsafe_b64encode(message.as_string())}
	except errors.HttpError, error:
		print error

if __name__ == '__main__':

	try:
		service = certificate()
		user_profile_response = service.users().getProfile(userId='me').execute()
		print ('messagesTotal:'+str(user_profile_response["messagesTotal"]))

		"""
		mail_from = raw_input("mail from :")
		mail_to = raw_input("mail to :")
		mail_subject = raw_input("subject :")
		mail_message = raw_input("content :")
		path = raw_input("file_path :")

		mail = create_message_with_attachment(mail_from,mail_to,mail_subject,mail_message,path)
		send_message(service,'me',mail)
		
		mail = create_message("purpledoor4921@gmail.com","purpledoor4921@gmail.com","test case","test")
		send_message(service,'me',mail)
		
		query_subject = raw_input("subject : ")
		query_result = query_mail(service, 'me', "subject:"+query_subject)
		for mail_id in query_result['messages']:
			#print('mail id : '+str(mail_id['id']))
			download_files(service, 'me', mail_id['id'])
		"""
		
	except :
		#print('An error occured :',error)
		pass