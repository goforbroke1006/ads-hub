import json
from os.path import expanduser

from facebookads import FacebookAdsApi
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser
from facebookads.adobjects.adspixel import AdsPixel
from facebookads.objects import Page

auth_config = json.load(
    open(expanduser("~") + '/.ads-hub/fb-token', 'r')
)

# https://developers.facebook.com/docs/marketing-api/insights-api
# https://developers.facebook.com/docs/marketing-api/access/#basic_application

# app_id = auth_config["app_id"]
# app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

FacebookAdsApi.init(access_token=access_token)

# print AdsPixel('772856039569351').get_ad_accounts(1034901646550640)
# print AdsPixel('772856039569351').get_stats()

# page = Page(122961418485088)
# print page.get_leadgen_forms()

account = AdAccount('act_1868848106489319')
users = account.get_users()
for user in users:
    print(user[AdAccountUser.Field.id])
