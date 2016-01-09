#!/usr/bin/python
# -*- coding: utf8 -*-
##########################################################
#it's runing python 2.7
#first need to install google python api by using
#pip install --upgrade google-api-python-client
#or other metheds
##########################################################
import gmail_connecter, join, split
import json,os, shutil, re
import glob

if __name__ == "__main__":
	gmail_service = gmail_connecter.certificate()
	print ('請選擇要做的工作\n(1)寄信\n(2)搜尋並下載檔案\n(3)郵件清單\n(4)合併檔案')
	case = raw_input('>')
	if case == '1':
		#mail_from = raw_input("mail from :")
		mail_from = ''
		mail_to = raw_input("mail to :")
		mail_subject = raw_input("subject :")
		mail_message = raw_input("content :")
		has_attachment = raw_input('需上傳檔案嗎(Y/n)?')
		size = 1024*1000
		path_array = []
		tmp_dir=""
		if has_attachment.lower() == 'n' or has_attachment.lower() == 'no':
			mail = gmail_connecter.create_message(mail_from,mail_to,mail_subject,mail_message)

		else:
			print ('file choose end please double enter')
			while 1:
				path = raw_input("file_path :")
				if not path :
					break
				rmdir = split.split(path,'.tmp',size)
				for temp in rmdir[0]:
					path_array.append(temp)
					tmp_dir=rmdir[1]
				#path_array.append(path)
			mail = gmail_connecter.create_message_with_attachment(mail_from,mail_to,mail_subject,mail_message,path_array)
			shutil.rmtree(tmp_dir)
		print ('sending')
		gmail_connecter.send_message(gmail_service,'me',mail)
		
	elif case == '2':
		subject = raw_input("subject : ")
		subject = "subject:"+subject
		mail_id_query_response = gmail_connecter.query_mail(gmail_service,'me',subject)
		for mail_id in mail_id_query_response['messages']:
			mails_detail = gmail_connecter.get_mail_detail(gmail_service,'me',mail_id['id'])
			for payload in mails_detail['payload']['headers']:
				#print (json.dumps(payload))
				if payload['name'] == 'From':
					print ("From : "+str(payload['value'].encode('utf-8')))
				if payload['name'] == 'To':
					print ("To : "+str(payload['value'].encode('utf-8')))
				if payload['name'] == "Subject":
					print ("Subject : "+str(payload['value'].encode('utf-8')))
			print ('content:')
			print (mails_detail['snippet']+"\n")
			gmail_connecter.download_files(gmail_service, 'me', mail_id['id'])
		parts = os.listdir(os.getcwd())
		temp_dir = '.tmp'
		index = 1
		while 1:
			if not os.path.exists(temp_dir):
				os.mkdir(temp_dir)
				break
			else :
				temp_dir = temp_dir+str(index)

		for i in parts:
			if re.match('.*_1',i):
				file_name = i
				file_name = (file_name.split('.',1)[1]).split('_1',-1)[0]
				print file_name
			if re.match('.*_[0-999]',i):
				shutil.move(i,temp_dir+'/'+i)
		join.join(temp_dir,file_name)
		shutil.rmtree(temp_dir)
	elif case == '3':
		max_result = raw_input('input max result:')
		print ('mail list:')
		mail_id_query_response = gmail_connecter.list_mail(gmail_service,'me',max_result)
		for mail_id in mail_id_query_response['messages']:
			mails_detail = gmail_connecter.get_mail_detail(gmail_service,'me',mail_id['id'])
			#print (json.dumps(mails_detail))
			for payload in mails_detail['payload']['headers']:
				#print (json.dumps(payload))
				if payload['name'] == "Subject":
					print ("Subject : "+str(payload['value'].encode('utf-8')))
	elif case == '4':
		fromdir = raw_input('欲還原檔資料夾位置')
		tofile = raw_input('file name :')
		join.join(fromdir,tofile)
	else:
		print ('exit')

	