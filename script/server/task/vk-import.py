#!/usr/bin/python

import os
import sys
import time
from datetime import datetime, timedelta
from random import randint

from connector import vkontakte_api
from script.server.csv_writer import CsvExportWriter

account_id, access_token, import_dir, = sys.argv[1:]

if import_dir.endswith('/'):
    import_dir = import_dir[:-1]

ads_client = vkontakte_api.AdsService(access_token)
# ads_client.debug_mode = True

# database_config = config('database.ini', 'postgresql')
# repository = AdsRepository(database_config, "vkontakte")

t = datetime.today()
writer = CsvExportWriter(
    target_directory=import_dir,
    provider_name="vk.com", date=t.strftime('%Y-%m-%d-%H-%M-%S'))

# print('Load all campaigns...')
campaigns_list = ads_client.get_campaigns(account_id)["response"]
# for campaign in campaigns_list:
#     start_time = int(campaign["start_time"]) \
#         if int(campaign["start_time"]) > 0 else int(campaign["create_time"])
#     stop_time = int(campaign["stop_time"]) \
#         if int(campaign["stop_time"]) > 0 else None
#     repository.save_campaign(
#         campaign["id"],
#         campaign["name"],
#         start_time,
#         stop_time
#     )

for campaign in campaigns_list:

    time.sleep(randint(2, 6))

    # print('Load all advertising list...')
    ads_list = ads_client.get_ads(account_id, campaign_ids=(campaign['id'],), include_deleted=True)["response"]

    ads_ids_list = []
    for ad in ads_list:
        ads_ids_list.append(ad["id"])

    stat_response = ads_client.get_statistics(
        account_id, "ad", "day", ads_ids_list,
        datetime.today() - timedelta(days=30),
        datetime.today()
    )["response"]

    for stat_row in stat_response:
        stat = stat_row["stats"]
        for s in stat:
            campaign_name = campaign['name'].encode('utf-8')
            campaign_id = str(campaign['id'])
            writer.write(
                ga_medium='cmp',
                ga_campaign=campaign_name + ' | ' + campaign_id,
                ga_adwards_campaign_id=campaign['id'],

                ga_keyword=campaign_name,
                ga_ad_content=campaign_name,

                ga_ad_cost=(s["spent"] if "spent" in s else 0),
                ga_ad_clicks=(s["clicks"] if "clicks" in s else 0),
                ga_impressions=(s["impressions"] if "impressions" in s else 0),

                ga_ad_group='ADSHUB | ' + campaign_id,
                ga_ad_slot=0,
                ga_date=datetime.strptime(s["day"], "%Y-%m-%d"),

                ga_import_behavior=None,
            )

print os.path.abspath(writer.file_path)
exit(0)

for ad in ads_list:
    # repository.save_advertising(
    #     ad["id"],
    #     ad["title"],
    #     ad["link_url"],
    #     ad["campaign_id"],
    #     None
    # )

    campaign_name = 'none'
    for c in campaigns_list:
        if c['id'] == ad['campaign_id']:
            campaign_name = c['name']
            break

    time.sleep(randint(2, 6))

    print('    Update stat for %d ...' % int(ad["id"]))
    stat_response = ads_client.get_statistics(
        account_id, "ad", "day", (ad["id"],),
        datetime.today() - timedelta(days=7),
        datetime.today()
    )["response"]

    stat_row = stat_response[0]
    stat = stat_row["stats"]

    for s in stat:
        writer.write(
            ga_medium='cmp',
            ga_campaign=campaign_name + '|' + ad.campaign_id,

            ga_ad_cost=(s["spent"] if "spent" in s else 0),
            ga_ad_clicks=(s["clicks"] if "clicks" in s else 0),
            ga_impressions=(s["impressions"] if "impressions" in s else 0),

            ga_date=datetime.strptime(s["day"], "%Y-%m-%d")
        )

        # repository.save_statistics_day(
        #     stat_row["id"],
        #     datetime.strptime(s["day"], "%Y-%m-%d"),
        #     s["spent"] if "spent" in s else 0,
        #     s["impressions"] if "impressions" in s else 0,
        #     s["clicks"] if "clicks" in s else 0,
        # )

print os.path.abspath(writer.file_path)
