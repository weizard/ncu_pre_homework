from dropbox import DropboxOAuth2FlowNoRedirect
import dropbox
import json
import os.path

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

#user login
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

# list (root) folder
dbx = dropbox.Dropbox(access_token)

#print dbx.users_get_current_account()
for name in dbx.files_list_folder('').entries:
	print name.name

#file down load
"""
down_path = '/physic/ch21_m1.pdf'
local_path = os.path.expanduser('~')
local_path = os.path.join(local_path,"Desktop",'ch21_m1.pdf')
md = dbx.files_download_to_file(local_path,down_path)
#print md
upload_file = os.path.join(os.path.expanduser('~'),'Desktop','cover.jpg')
"""
#file upload
"""
with open(upload_file,'rb') as f:
	upload_md = dbx.files_upload(f,'/cover.jpg')
print upload_md
"""
#create folder
"""
md = dbx.files_create_folder('/test_folder')
print md
"""