from dropbox import DropboxOAuth2FlowNoRedirect
import dropbox
import json
import os
import re

APP_KEY = "5gk15fxocs1nwxp"
APP_SECRET = "rmsjn87kru02ckk"

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

"""
authorize_url = auth_flow.start()
print "1. Go to: " + authorize_url
print "2. Click \"Allow\" (you might have to log in first)."
print "3. Copy the authorization code."
auth_code = raw_input("Enter the authorization code here: ").strip()
"""
def get_dropbox_access():
	try:
		#access_token, user_id = auth_flow.finish(auth_code)
		data = {}
		#data['access_token'] = access_token
		#data['user_id'] = user_id
		if os.path.exists('dropbox_access.json'):
			with open('dropbox_access.json','r') as r_access:
				data = json.load(r_access)
				access_token = data['access_token']
				user_id = data['user_id']
		else:
			authorize_url = auth_flow.start()
			print "1. Go to: " + authorize_url
			print "2. Click \"Allow\" (you might have to log in first)."
			print "3. Copy the authorization code."
			auth_code = raw_input("Enter the authorization code here: ").strip()
			access_token, user_id = auth_flow.finish(auth_code)
			data['access_token'] = access_token
			data['user_id'] = user_id
			with open('dropbox_access.json','w') as w_access:
				json.dump(data,w_access)
	except Exception, e:
	    print('Error: %s' % (e,))
	    pass

	dbx = dropbox.Dropbox(access_token)
	return dbx

def list_folder(dbx,dropbox_path):
	return dbx.files_list_folder(dropbox_path).entries

def files_download(dbx,local_path,download_path):
	md = dbx.files_download_to_file(local_path,download_path)
	return md

def files_upload(dbx,upload_file,dropbox_path):
	with open(upload_file,'rb') as f:
		upload_md = dbx.files_upload(f,dropbox_path)
	return upload_md

def folder_create(dbx,dropbox_path):
	md = dbx.files_create_folder(dropbox_path)
	return md

def main():
	print "You can use method: ls, download, upload, mkdir.\nAnd use -help, ? to look up how to use it."
	input_string = raw_input(">>")
	do = input_string.split(" ")
	dbx = get_dropbox_access()
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
		files_in_folder = list_folder(dbx,dropbox_path)
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
			print "\tDownload the file form dropbox to local."
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
		file_download = files_download(dbx,local_path,dropbox_path)
	elif do[0]=="upload":
		#upload the file to dropbox
		if len(do)<=1 or do[1] == "-help" or do[1] == "?":
			print "NAME"
			print "\tupload -- upload the file to dropbox"
			print ""
			print "SYNOPSIS"
			print "\tupload \033[4mdropbox path\033[0m \033[4mloacl path\033[0m"
			print ""
			print "DESCRIPTION"
			print "\tupload the file to dropbox form local."
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
		file_upload = files_upload(dbx,local_path,dropbox_path)
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
			dropbox_folder_create = folder_create(dbx,dropbox_path)
	else:
		#help
		print "You can use method ls, download, upload.\nAnd each method you can use -help or ? to look up the manual."

if __name__ == '__main__':
	main()
	"""
	dbx = get_dropbox_access()
	files_in_folder = list_folder(dbx,'')
	for files in files_in_folder:
		print files.name
	#all method args => dropbox_object, local_files, dropbox_files
	local_path = os.path.expanduser('~')
	local_path = os.path.join(local_path,"Desktop",'ch21_m1.pdf')
	file_download = files_download(dbx,local_path,'/physic/ch21_m1.pdf')
	local_path = os.path.expanduser('~')
	local_path = os.path.join(local_path,"Desktop",'cover.jpg')
	file_upload = files_upload(dbx,local_path,'/cover.jpg')
	dropbox_folder_create = folder_create(dbx,'/test_folder')
	"""
	#print dbx.users_get_current_account()
	

	"""
	s = raw_input("input:")
	print s.split(" ")
	"""
	#print os.path.expanduser('/')
	#file down load
	"""
	down_path = '/physic/ch21_m1.pdf'
	local_path = os.path.expanduser('~')
	local_path = os.path.join(local_path,"Desktop",'ch21_m1.pdf')
	md = dbx.files_download_to_file(local_path,down_path)
	#print md
	"""
	#file upload
	"""
	upload_file = os.path.join(os.path.expanduser('~'),'Desktop','cover.jpg')
	
	with open(upload_file,'rb') as f:
		upload_md = dbx.files_upload(f,'/cover.jpg')
	print upload_md
	"""
	#create folder
	"""
	md = dbx.files_create_folder('/test_folder')
	print md
	"""