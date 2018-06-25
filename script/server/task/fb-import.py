import json
import sys
import time
from random import randrange

from dateutil.parser import parse
from facebook_business import FacebookAdsApi

import connector.facebook_api
from script.server.base import config
from script.server.repository import AdsRepository

auth_config = json.load(open("./.auth/fb-token", "r"))

# https://developers.facebook.com/docs/marketing-api/insights-api
# https://developers.facebook.com/docs/marketing-api/access/#basic_application

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

campaign_id = 'act_%s' % sys.argv[1]

database_config = config("database.ini", "postgresql")
repository = AdsRepository(database_config, "facebook")

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret,
                    access_token=access_token,
                    account_id=campaign_id)

print "Loading campaigns blocks..."
campaigns = connector.facebook_api.get_campaigns()

for c in campaigns:
    start_time = parse(c['start_time'])
    stop_time = parse(c['stop_time']) if 'stop_time' in c else None
    repository.save_campaign(
        c.get_id(),
        c['name'],
        start_time,
        stop_time,
    )
    print "Save campaign \"%s\"..." % c['name']

    print "Loading advertising blocks..."
    ads_list = connector.facebook_api.get_ads(c)

    for ad in ads_list:
        repository.save_advertising(
            ad.get_id(),
            ad['name'],
            '',
            c.get_id(),
        )
        print "Save advertising \"%s\"..." % ad['name']

        time.sleep(randrange(2, 6))

        print "Load statistics..."
        insights = connector.facebook_api.get_insights(ad)

        for insight in insights:
            repository.save_statistics_day(
                ad.get_id(),
                parse(insight['date_start']),
                insight['spend'],
                insight['impressions'],
                insight['unique_clicks'],
            )
