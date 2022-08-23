import os
import json


def get_creds(path):
	credentials_path = os.path.join(os.path.dirname(__file__), path)
	if not os.path.exists(credentials_path):
		error = "credentials.json file not found at %s" % credentials_path
		raise FileNotFoundError(error)
	c = open(credentials_path)
	creds = json.load(c)
	return creds