#!/usr/bin/python
# -*- coding: utf8 -*-
##########################################################
#it's runing python 2.7
#first need to install google& dropbox python api by using
#pip install --upgrade google-api-python-client
#pip install dropbox
#or other metheds
##########################################################
import gmail_connecter, join, split
import json,os, shutil, re
import glob
import dropbox_connecter

if __name__ == "__main__":
	gmail_service = gmail_connecter.certificate()
	print ('請選擇要做的工作\n(1)寄信\n(2)搜尋並下載檔案\n(3)郵件清單\n(4)合併檔案\n(5)Dropbox')
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
				path = os.path.expanduser(path)
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
	elif case == '5':
		print "You can use method: ls, download, upload, mkdir.\nAnd use -help, ? to look up how to use it."
		input_string = raw_input(">>")
		do = input_string.split(" ")
		dbx = dropbox_connecter.get_dropbox_access()
		if do[0]=="ls":
			#list files in the folder
			if len(do) <= 1 :
				do.append("")
			if do[1] == "-help" or do[1] == "?":
				#ls help
				print "NAME"
				print "\tls -- list dropbox directory"
				print ""
				print "SYNOPSIS"
				print "\tls \033[4mdropbox path\033[0m"
				print ""
				print "DESCRIPTION"
				print "\tList files or folder in dropbox."
			else:
				if not do[1] == "":
					dropbox_path = do[1]
					if dropbox_path == "/":
						dropbox_path == ""
					else:
						if dropbox_path[0] == "~":
							#dropbox_path = dropbox_path.replace("~","",1)
							dropbox_path = re.sub(r'[^a-zA-Z0-9]',"",dropbox_path,1)
						if not dropbox_path[0]=="/":
							dropbox_path = "/"+dropbox_path
				else:
					dropbox_path = ""
			#print "dropbox_path:"+dropbox_path
			files_in_folder = dropbox_connecter.list_folder(dbx,dropbox_path)
			for files in files_in_folder:
				print files.name
		elif do[0]=="download":
			#download the file from dropbox
			if len(do)<=1 or do[1] == "-help" or do[1] == "?":
				print "NAME"
				print "\tdownload -- download the file from dropbox"
				print ""
				print "SYNOPSIS"
				print "\tdownload \033[4mdropbox path\033[0m \033[4mloacl path\033[0m"
				print ""
				print "DESCRIPTION"
				print "\tDownload the file form dropbox to local.\n\tIf the file be split user can download the *.split folder, \n\tsystem will auto combine the file."
			else:
				if not do[1] == "":
					dropbox_path = do[1]
					if dropbox_path == "/":
						dropbox_path == ""
					else:
						if dropbox_path[0] == "~":
							#dropbox_path = dropbox_path.replace("~","",1)
							dropbox_path = re.sub(r'[^a-zA-Z0-9]',"",dropbox_path,1)
						if not dropbox_path[0]=="/":
							dropbox_path = "/"+dropbox_path
				else:
					dropbox_path = ""
				local_path = os.path.expanduser(do[2])
				local_path_exist = os.path.isfile(local_path)
				#print "dropbox path:" + dropbox_path
				#print "local path:" + local_path
				#print local_path_exist
				temp_dir = os.path.expanduser(".file_split_app_temp")
				if (dropbox_path.split("/")[-1]).split(".")[-1] == 'split':
					if not os.path.exists(temp_dir):
						os.mkdir(temp_dir)
					else:
						for fname in os.listdir(temp_dir):
							os.remove(os.path.join(temp_dir, fname))
					files_in_folder = dropbox_connecter.list_folder(dbx,dropbox_path)
					for a in files_in_folder:
						#print "in folder:"+a.name
						#print (dropbox_path+"/"+a.name)
						file_download = dropbox_connecter.files_download(dbx,(temp_dir+"/"+a.name),(dropbox_path+"/"+a.name))
					join.join(temp_dir,local_path)
				else:
					file_download = dropbox_connecter.files_download(dbx,local_path,dropbox_path)
				print "download complete"
		elif do[0]=="upload":
			#upload the file to dropbox
			size = 1024*1000
			path_array = []
			tmp_dir=""
			if len(do)<=1 or do[1] == "-help" or do[1] == "?":
				print "NAME"
				print "\tupload -- upload the file to dropbox"
				print ""
				print "SYNOPSIS"
				print "\tupload \033[4mdropbox path\033[0m \033[4mloacl path\033[0m"
				print ""
				print "DESCRIPTION"
				print "\tupload the file to dropbox form local.\n\tIf use the function split, file will put in defaul folder\n\t(file_split_app)."
			else:
				if not do[1] == "":
					dropbox_path = do[1]
					if dropbox_path == "/":
						dropbox_path == ""
					else:
						if dropbox_path[0] == "~":
							#dropbox_path = dropbox_path.replace("~","",1)
							dropbox_path = re.sub(r'[^a-zA-Z0-9]',"",dropbox_path,1)
						if not dropbox_path[0]=="/":
							dropbox_path = "/"+dropbox_path
				else:
					dropbox_path = ""
				local_path = os.path.expanduser(do[2])
				local_path_exist = os.path.isfile(local_path)
				#print "dropbox path:" + dropbox_path
				#print "local path:" + local_path
				#print local_path_exist
				split_check = raw_input("是否要分割上傳(Y/n)?")
				if split_check.lower() == 'y' or split_check.lower() =='yes':
					dropbox_path = "/file_split_app/"+local_path.split("/")[-1]+".split"
					try:
						dropbox_connecter.folder_create(dbx,dropbox_path)
					except:
						print "folder (files) exist or upload error"
					rmdir = split.split(local_path,'.tmp',size)
					for temp in rmdir[0]:
						path_array.append(temp)
						tmp_dir=rmdir[1]
					for temp_path in path_array:
						#print temp_path
						dropbox_connecter.files_upload(dbx,temp_path,(dropbox_path+"/"+temp_path.split("/")[-1]))
					#file_upload = dropbox_connecter.files_upload(dbx,local_path,dropbox_path)
					shutil.rmtree(tmp_dir)
				else:
					file_upload = dropbox_connecter.files_upload(dbx,local_path,dropbox_path)
				print "upload complete"
		elif do[0]=="mkdir":
			if len(do)<=1 or do[1] == "-help" or do[1] == "?":
				print "NAME"
				print "\tmkdir -- create folder in dropbox"
				print ""
				print "SYNOPSIS"
				print "\tmkdir \033[4mdropbox folder path\033[0m"
				print ""
				print "DESCRIPTION"
				print "\tCreate a foler in dropbox."
			else:
				if not do[1] == "":
					dropbox_path = do[1]
					if dropbox_path == "/":
						dropbox_path == ""
					else:
						if dropbox_path[0] == "~":
							#dropbox_path = dropbox_path.replace("~","",1)
							dropbox_path = re.sub(r'[^a-zA-Z0-9]',"",dropbox_path,1)
						if not dropbox_path[0]=="/":
							dropbox_path = "/"+dropbox_path
				else:
					dropbox_path = ""
				dropbox_folder_create = dropbox_connecter.folder_create(dbx,dropbox_path)
		else:
			#help
			print "You can use method ls, download, upload.\nAnd each method you can use -help or ? to look up the manual."
	else:
		print ('exit')

	