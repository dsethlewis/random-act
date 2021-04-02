#!/usr/bin/python3

import activity
from microsoftgraph.client import Client

client = Client("dsethlewis@gmail.com", "johnjaco8")
url = client.authorization_url(redirect_uri, scope, state=None)