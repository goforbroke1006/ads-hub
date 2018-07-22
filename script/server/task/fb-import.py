import sys
import time
from datetime import datetime
from random import randrange

from dateutil.parser import parse
from facebook_business import FacebookAdsApi

import connector.facebook_api
from script.server.csv_writer import CsvExportWriter

campaign_id, access_token, import_dir, = sys.argv[1:]
campaign_id = 'act_%s' % campaign_id
if import_dir.endswith('/'):
    import_dir = import_dir[:-1]

# database_config = config("database.ini", "postgresql")
# repository = AdsRepository(database_config, "facebook")

t = datetime.today()
writer = CsvExportWriter(
    target_directory=import_dir,
    provider_name="facebook.com", date=t.strftime('%Y-%m-%d-%H-%M-%S'))

FacebookAdsApi.init(
    access_token=access_token,
    account_id=campaign_id)

# print "Loading campaigns blocks..."
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
    camp_name = c['name'].encode('utf-8')
    # print "Save campaign \"%s\"..." % camp_name

    # print "Loading advertising blocks..."
    ads_list = connector.facebook_api.get_ads(c)

    for ad in ads_list:
        # repository.save_advertising(
        #     ad.get_id(),
        #     ad['name'],
        #     '',
        #     c.get_id(),
        # )
        # print "Save advertising \"%s\"..." % ad['name']

        time.sleep(randrange(2, 6))

        # print "Load statistics..."
        insights = connector.facebook_api.get_insights(ad)

        for insight in insights:

            medium = ''
            if 'cpc' in insight:
                medium = 'cpc'
            elif 'cpm' in insight:
                medium = 'cpm'
            elif 'cpp' in insight:
                medium = 'cpp'
            elif 'ctr' in insight:
                medium = 'ctr'

            camp_id = c.get_id().encode('utf-8')
            writer.write(
                ga_medium=medium,
                ga_campaign=camp_name + '|' + camp_id,
                ga_adwards_campaign_id=ad.get_id(),

                ga_keyword=camp_name,
                ga_ad_content=camp_name,

                ga_ad_cost=insight['spend'].encode('utf-8'),
                ga_ad_clicks=insight['unique_clicks'].encode('utf-8'),
                ga_impressions=insight['impressions'].encode('utf-8'),

                ga_ad_group='ADSHUB | ' + camp_id,
                ga_ad_slot=0,
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

print writer.file_path
