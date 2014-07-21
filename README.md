Rpas-py
=======

RPAS REST API Client for Python

#Quick start

```python
import rpas

#RPAS.__init__(token, username, password, api_version="v1")

client = rpas(None, "username", "pw")

pprint(client.taxonomies.name)
pprint(client.taxonomies.list({'query': 'qv'}))
pprint(client.taxonomies.select("id", {'query': 'qv'}))
```
