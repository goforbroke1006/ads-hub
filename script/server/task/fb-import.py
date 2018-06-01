import json
from os.path import expanduser
import facebook_business

# from facebookads import FacebookAdsApi

from facebook_business import FacebookAdsApi

from connector.facebook_api import some_import_method

auth_config = json.load(
    open(expanduser("~") + '/.ads-hub/fb-token', 'r')
)

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

# FacebookAdsApi.init(app_id, app_secret, access_token)
FacebookAdsApi.init(app_id, app_secret, access_token)

# some_import_method(122961418485088, access_token)
some_import_method(1034901646550640, access_token)
