import json
import sys
import time
from random import randrange

from dateutil.parser import parse
from facebook_business import FacebookAdsApi

import connector.facebook_api
from script.server.base import config
from script.server.csv_writer import CsvExportWriter
from script.server.repository import AdsRepository
from datetime import datetime

auth_config = json.load(open("./.auth/fb-token", "r"))

# https://developers.facebook.com/docs/marketing-api/insights-api
# https://developers.facebook.com/docs/marketing-api/access/#basic_application

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

campaign_id = 'act_%s' % sys.argv[1]

# database_config = config("database.ini", "postgresql")
# repository = AdsRepository(database_config, "facebook")

t = datetime.today()
writer = CsvExportWriter(
    target_directory='import',
    provider_name="facebook.com", date=t.strftime('%Y-%m-%d'))

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret,
                    access_token=access_token,
                    account_id=campaign_id)

print "Loading campaigns blocks..."
campaigns = connector.facebook_api.get_campaigns()

for c in campaigns:
    start_time = parse(c['start_time'])
    stop_time = parse(c['stop_time']) if 'stop_time' in c else None
    # repository.save_campaign(
    #     c.get_id(),
    #     c['name'],
    #     start_time,
    #     stop_time,
    # )
    print "Save campaign \"%s\"..." % c['name']

    print "Loading advertising blocks..."
    ads_list = connector.facebook_api.get_ads(c)

    for ad in ads_list:
        # repository.save_advertising(
        #     ad.get_id(),
        #     ad['name'],
        #     '',
        #     c.get_id(),
        # )
        print "Save advertising \"%s\"..." % ad['name']

        time.sleep(randrange(2, 6))

        print "Load statistics..."
        insights = connector.facebook_api.get_insights(ad)

        for insight in insights:
            writer.write(
                ga_medium='cmp',
                ga_campaign=c['name'] + '|' + c.get_id(),
                ga_adwards_campaign_id=None,

                ga_keyword=None,
                ga_ad_content=None,

                ga_ad_cost=insight['spend'],
                ga_ad_clicks=insight['unique_clicks'],
                ga_impressions=insight['impressions'],

                ga_ad_group=None,
                ga_ad_slot=None,
                ga_date=parse(insight['date_start']),

                ga_import_behavior=None,
            )

            # repository.save_statistics_day(
            #     ad.get_id(),
            #     parse(insight['date_start']),
            #     insight['spend'],
            #     insight['impressions'],
            #     insight['unique_clicks'],
            # )
