import requests
from requests.auth import HTTPBasicAuth
import json

# TODO:
#  - Paginate the rules and do this on paginated rules


_HOST = 'https://0.0.0.0:5601'
_USERNAME = 'elastic'
_PASSWORD = 'some_password'

headers = {
    'kbn-xsrf': 'elk-tls-docker',
    'Content-Type': 'application/json'
}


def do_get_request(endpoint):
    response = requests.get(_HOST + ENDPOINT,
        headers=headers,
        auth=HTTPBasicAuth(_USERNAME, _PASSWORD),
        verify=False)
    return response


def do_patch_request(endpoint, data):
    response = requests.patch(_HOST + ENDPOINT,
        headers=headers,
        auth=HTTPBasicAuth(_USERNAME, _PASSWORD),
        data=data,
        verify=False)
    return response


rules_response = do_get_request("/api/detection_engine/rules/_find?per_page=600")
rules_json = json.loads(rules_response.text)

rule_updates = []
for rule in rules_json['data']:
    rule_id = rule['rule_id']
    # You have to add your custom rule action. Create the connector first and add the id to the 'id' key. A sample body is provided for you.
    rule_action = [{'group': 'default', 'id': '6b4df540-2c5b-11ec-ac4d-7d35dd64726e', 'params': {'body': '{\n    "text": "<b>{{context.rule.name}}</b> fired @ {{date}}<br><br>{{context.rule.description}}<br><br><a href=\\"{{kibanaBaseUrl}}\\">Take Me to Kibana</a>",\n   "format": "html",\n   "displayName": "Elk Webhook Notifs",\n   "avatar_url": "http://i.imgur.com/IDOBtEJ.png"\n }'}, 'action_type_id': '.webhook'}]
    updated_rule = {"rule_id": rule_id, "actions": rule_action}
    rule_updates.append(updated_rule)



# with open('rule_updates.json', 'w') as f:
#    json.dump(rule_updates, f)

patch_response = do_patch_request("/api/detection_engine/rules/_bulk_update", json.dumps(rule_updates))
