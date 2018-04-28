import urllib2
import json
import sys
from os.path import expanduser
from datetime import datetime

# period = day | month | overall

f = open(expanduser("~") + '/.adv-hub/vk-token', 'r')
cfg = json.load(f)

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

try:
    response = urllib2.urlopen(url)
    data = json.load(response)

    #f = open("./qwere.txt", 'w+')
    #f.write(str(data))
    #f.close()

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

