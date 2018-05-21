#!/usr/bin/python
import ConfigParser
import json
import sys
from datetime import datetime
from os.path import expanduser
from random import randint
from time import sleep

import psycopg2

from vkontakteapi import ads


def config(filename, section):
    parser = ConfigParser.ConfigParser()
    parser.read(filename)

    data = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            data[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return data


def connect(params):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()
    #        print('Database connection closed.')
    return conn



cfg = json.load(open(expanduser("~") + '/.ads-hub/vk-token', 'r'))
ads_client = ads(cfg["access_token"])

ids_types = ["ad", "campaign", "client", "office", ]

account_id = int(sys.argv[1])

ads_list = ads_client.get_ads_layout(account_id)
print(ads_list)

conn = connect(config('database.ini', 'postgresql'))
cur = conn.cursor()

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

    values = cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ", (
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
    result = cur.execute(query)
    print(result)
    conn.commit()
cur.close()
conn.close()
