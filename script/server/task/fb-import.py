import json
from os.path import expanduser

# from facebookads import FacebookAdsApi
# from facebookads.adobjects.adaccount import AdAccount
# from facebookads.adobjects.adaccountuser import AdAccountUser
import sys
from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adspixel import AdsPixel
from facebook_business.adobjects.campaign import Campaign

from connector.facebook_api import get_statistics_for_today, get_campaigns
from script.server.base import config
from script.server.repository import AdsRepository

auth_config = json.load(
    open(expanduser("~") + '/.ads-hub/fb-token', 'r')
)

# https://developers.facebook.com/docs/marketing-api/insights-api
# https://developers.facebook.com/docs/marketing-api/access/#basic_application

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

campaign_id = 'act_%s' % sys.argv[1]

# database_config = config('database.ini', 'postgresql')
# repository = AdsRepository(database_config, "facebook")

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret,
                    access_token=access_token,
                    account_id=campaign_id)

get_campaigns()
