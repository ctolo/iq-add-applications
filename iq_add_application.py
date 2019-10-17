import requests
import argparse

iq_session = requests.Session()
iq_url = ""

def main():
	global iq_url
	parser = argparse.ArgumentParser(description='Add Applications to IQ')
	parser.add_argument('-a','--auth', default="admin:admin123", required=False)
	parser.add_argument('-u','--url', default="http://localhost:8070", required=False)
	parser.add_argument('-i','--publicId', required=True)
	parser.add_argument('-n','--name', default="", required=False)
	parser.add_argument('-o','--orgName', default="Sandbox Organization", required=False)


	args = vars(parser.parse_args())
	creds = args["auth"].split(":")
	iq_session.auth = requests.auth.HTTPBasicAuth(creds[0], creds[1] )
	iq_url = args["url"]
	name = args["name"] if len(args["name"]) else args["publicId"]
	#-------------------
	#check is application is in IQ.
	app = get_Application(args["publicId"])

	#If not we need to locate the organizationId first then add the app to IQ using the publicId, name, and organizationId.  
	#This can be customized to add app categories and users access.
		organizationId = get_Organizations(organization)
		response = add_Application(args["publicId"], name, organizationId)
		print (f"Added: {response['id']}")

	else:
		a = app[0]
		print (f"Found: {a['id']}")
		# print (f"app found\nDeleting app: {a['name']}")
		# print (delete_Application( a['id']) )

#----------------------------------------------------------------------
def get_Organizations(org="Sandbox Organization"):
	p=iq_session.get(f'{iq_url}/api/v2/organizations').json()
	for o in p["organizations"]:
		if org in [o["id"], o["name"]]:
			return o["id"]
	print("error finding organization")
	raise SystemExit

def get_Application(publicId="sandbox-application"):
	if len(publicId) > 0:
		url = f'{iq_url}/api/v2/applications?publicId={publicId}'
		response = iq_session.get(url)
		if response.status_code != requests.codes.ok:
			print(f"error with get_Application().\n{response.text}"); raise SystemExit
		return response.json()["applications"]

def add_Application(publicId, name, organizationId):
	data = {"publicId": publicId, "name": name, "organizationId": organizationId}
	response = iq_session.post( f'{iq_url}/api/v2/applications', json=data)
	if response.status_code != requests.codes.ok:
		print(f"error with add_Application().\n{response.text}"); raise SystemExit
	return response.json()

def delete_Application(applicationInternalId=""):
	if len(applicationInternalId)>0:
		url = f'{iq_url}/api/v2/applications/{applicationInternalId}'
		response = iq_session.delete(url)
		return response
#----------------------------------------------------------------------
if __name__ == "__main__": main() #call main function on load.




