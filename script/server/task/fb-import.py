import json
from os.path import expanduser

import facebookads
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser

auth_config = json.load(
    open(expanduser("~") + '/.ads-hub/fb-token', 'r')
)

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

facebookads.FacebookAdsApi.init(app_id, app_secret, access_token)

account = AdAccount('act_1868848106489319')
users = account.get_users()
for user in users:
    print(user[AdAccountUser.Field.id])
