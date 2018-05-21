#!/usr/bin/python

import json
import sys
import os
from datetime import datetime
from os.path import expanduser
from random import randint
from time import sleep

import connector
from script.server.base import config
from script.server.repository import AdsRepository

account_id = int(sys.argv[1])

cfg = json.load(open(expanduser("~") + '/.ads-hub/vk-token', 'r'))
database_config = config('database.ini', 'postgresql')
# connection = connect(database_config)
# cursor = connection.cursor()
repository = AdsRepository(database_config, "vkontakte")
ads_client = connector.vkontakte_api.AdsService(cfg["access_token"])

ads_list = ads_client.get_ads_layout(account_id)
print(ads_list)
os._exit(0)

for row in ads_list["response"]:
    sleep(randint(2, 6))

    statistics = ads_client.get_statistics(
        account_id, "ad", "day", (row["id"],),
        datetime.now().replace(day=1))["response"]

    statistics = statistics[0]["stats"][0] if len(statistics[0]["stats"]) > 0 \
        else {
        "spent": 0,
        "impressions": 0,
        "clicks": 0,
    }

    values = cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ", (
        "vkontakte", 0, datetime.now(), "????",
        row["id"], row["title"], row["link_url"],
        '{}',
        float(statistics["spent"]) if "spent" in statistics else None,
        statistics["impressions"] if "impressions" in statistics else None,
        statistics["clicks"] if "clicks" in statistics else None,
        0
    ))
    query = "INSERT INTO advertising VALUES " + values + ";"
    print(query)
    result = cursor.execute(query)
    print(result)
    connection.commit()

cursor.close()
connection.close()
