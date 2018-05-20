#!/usr/bin/python

import urllib2
import json
import sys
from os.path import expanduser
from datetime import datetime
from configparser import ConfigParser
import psycopg2
from config import config

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

def connect(params):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
 
        # create a cursor
        #cur = conn.cursor()
        
        # execute a statement
        #print('PostgreSQL database version:')
        #cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        #db_version = cur.fetchone()
        #print(db_version)
       
        # close the communication with the PostgreSQL
        #cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    #finally:
    #    if conn is not None:
    #        conn.close()
    #        print('Database connection closed.')
    return conn
 
 
if __name__ == '__main__':
    conn = connect(config())

# period = day | month | overall

cfg = json.load(
    open(expanduser("~") + '/.adv-hub/vk-token', 'r')
)

ids_types = ["ad", "campaign", "client", "office",]

account_id = int(sys.argv[1])
#ids_type = sys.argv[2]
#if ids_type not in ids_types:
#    raise Exception("Unexpected ids_type: " + ids_type + ". Try to use next - " + str(ids_types).strip('[]'))

#url = "https://api.vk.com/method/ads.getStatistics?access_token=%saccount_id=%d&ids_type=%s&ids=&period=day&date_from=%s&date_to=%s" % (
#        cfg["access_token"], account_id, ids_type,
#        None, datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
#    )

url = "https://api.vk.com/method/ads.getAdsLayout?access_token=%s&account_id=%d&include_deleted=1&v=5.74" % (cfg["access_token"], account_id)
print url

# conn = psycopg2.connect(host="localhost:5432", database="ads_hub_db", user="root", password="12345678") # TODO: replace hardcode with params

cur = conn.cursor()
try:
    response = urllib2.urlopen(url)
    data = json.load(response)

    #f = open("./qwere.txt", 'w+')
    #f.write(str(data))
    #f.close()

    args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in data["response"])
    cur.execute("INSERT INTO table VALUES " + args_str)

    #print data
    for row in data["response"]:
        print row["age_restriction"]
        print row["ad_format"]
        print row["title"]
        print row["link_url"]
        print row["preview_link"]
        print row["campaign_id"]
        print row["image_src"]
        print row["cost_type"]
        print row["link_domain"]
        print row["id"]
        print "========== ========== ========== ========== =========="
except urllib2.HTTPError as ex:
    if ex.code == 400:
        print "You have not access for this account data"
    else:
        print ex.reason

