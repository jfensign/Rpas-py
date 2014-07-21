import urllib
import hashlib
import hmac
import base64
import requests
import json
import types

from requests.auth import HTTPBasicAuth
from pprint import pprint

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

class RpasException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class RpasResource:
	def __init__(self, rpas, resource):
		self.name = resource
		self.base_uri = "/".join([rpas.base_uri, resource])
		self.rpas_i = rpas

	def list(self, query={}):
		list_request = requests.get(self.base_uri,
									params=query,
									headers=self.rpas_i.rpas_headers)

		return list_request.json()

	def select(self, id, query={}):
		select_request = requests.get("/".join([self.base_uri, id]),
									  headers=self.rpas_i.rpas_headers)

		return select_request.json()



class RPAS:
	def __init__(self, token=None, username=None, password=None, api_version="v1"):

		self.api_version = api_version or "v1"

		#Append version to base_uri once domain is purchased.
		self.base_uri = "http://54.214.50.90"

		self.rpas_headers = {
		 'Accept': 'application/json',
		 'x-its-rpas': None,
		 'rpas-api-version': api_version
		}
		self.resources = {
			'users': 'users',
			'research_types': 'research_types',
			'taxonomies': 'taxonomies',
			'workflows': 'workflows',
			'roles': 'roles',
			'documents': 'documents',
			'products': 'products',
			'templates': 'templates',
			'organizations': 'organizations',
			'rated_items': 'rated_items',
			'lists': 'lists',
			'disclosures': 'disclosures',
			'disclosure_groups': 'disclosure_groups',
			'contacts': 'contacts',
			'contact_groups': 'contact_groups'
		}

		if username and password:
			auth_response = requests.post(self.base_uri + "/authenticate", 
									     auth=HTTPBasicAuth(username, password)).json()

			if auth_response["Auth"]:
				self.token = auth_response["Auth"]["RequestToken"]

		else:
			if token:
				self.token = token

		self.rpas_headers["x-its-rpas"] = self.token

		for resource in self.resources:
			setattr(self.__class__, resource, RpasResource(self, resource))