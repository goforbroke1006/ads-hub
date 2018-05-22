#!/usr/bin/python

import json
import sys
import time
from datetime import datetime, timedelta
from os.path import expanduser
from random import randint

import connector
from script.server.base import config
from script.server.repository import AdsRepository

account_id = int(sys.argv[1])

access_token = json.load(
    open(expanduser("~") + '/.ads-hub/vk-token', 'r')
)["access_token"]
ads_client = connector.vkontakte_api.AdsService(access_token)

database_config = config('database.ini', 'postgresql')
repository = AdsRepository(database_config, "vkontakte")

print('Load all campaigns...')
campaigns_list = ads_client.get_campaigns(account_id)["response"]
for campaign in campaigns_list:
    start_time = int(campaign["start_time"]) \
        if int(campaign["start_time"]) > 0 else int(campaign["create_time"])
    stop_time = int(campaign["stop_time"]) \
        if int(campaign["stop_time"]) > 0 else None

    repository.save_campaign(
        campaign["id"],
        campaign["name"],
        start_time,
        stop_time
    )

time.sleep(randint(2, 6))

print('Load all advertising list...')
ads_list = ads_client.get_ads_layout(account_id)["response"]
for ad in ads_list:
    repository.save_advertising(
        ad["id"],
        ad["title"],
        ad["link_url"],
        ad["campaign_id"],
        None
    )

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
        repository.save_statistics_day(
            stat_row["id"],
            datetime.strptime(s["day"], "%Y-%m-%d"),
            s["spent"] if "spent" in s else 0,
            s["impressions"] if "impressions" in s else 0,
            s["clicks"] if "clicks" in s else 0,
        )