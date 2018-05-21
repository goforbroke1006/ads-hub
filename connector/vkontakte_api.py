import json
import urllib2
from datetime import datetime

BASE_URL = "https://api.vk.com/method/"
API_VERSION = "5.74"


class VkApiError(Exception):
    def __init__(self, error_struct):
        self.code = error_struct['error_code']
        self.message = error_struct['error_msg']
        self.params = error_struct['request_params']

    def __str__(self):
        return "%d : %s" % (self.code, self.message)


class BaseClient:
    def __init__(self, access_token, debug_mode=False):
        self.access_token = access_token
        self.debug_mode = debug_mode
        pass

    def request(self, method_name, options=None):
        if options is None:
            options = dict()

        try:
            url = "%s%s?access_token=%s&v=%s&%s" \
                  % (
                      BASE_URL, method_name, self.access_token, API_VERSION,
                      '&'.join("%s=%s" % (key, val) for (key, val) in options.iteritems())
                  )

            if self.debug_mode:
                print url

            response = urllib2.urlopen(url)
            result = json.load(response)

            if self.debug_mode:
                print(result)

            if "error" in result:
                raise VkApiError(result["error"])

            return result

        except urllib2.HTTPError as ex:
            if self.debug_mode:
                print "Error %d: %s" % (ex.code, ex.reason)
            else:
                raise ex


class AdsService(BaseClient):
    def get_campaigns(self, account_id, client_id=None, include_deleted=True, campaign_ids=()):
        options = {
            "account_id": int(account_id),
            "include_deleted": int(include_deleted),
            "campaign_ids": (",".join("%s" % cid for cid in campaign_ids)),
        }
        if client_id is not None:
            options["client_id"] = client_id
        return self.request("ads.getCampaigns", options)

    def get_ads_layout(self, account_id,
                       client_id=None, include_deleted=True,
                       campaign_ids=(), ad_ids=(),
                       limit=200, offset=0):
        options = {
            "account_id": int(account_id),
            "include_deleted": int(include_deleted),
            "campaign_ids": ",".join("%s" % int(cmp_id) for cmp_id in campaign_ids),
            "ad_ids": ",".join("%s" % int(ad_id) for ad_id in ad_ids),
            "limit": int(limit),
            "offset": int(offset),
        }
        if client_id is not None:
            options["client_id"] = client_id
        return self.request("ads.getAdsLayout", options)

    def get_statistics(self, account_id, ids_type, period,
                       ids=(), date_from=None, date_to=None):
        ids_types = ["ad", "campaign", "client", "office", ]
        if ids_type not in ids_types:
            raise Exception("Unexpected ids_type: " + ids_type + ". "
                            + "Try to use next - " + str(ids_types).strip('[]'))

        period_range = ["day", "month", "overall"]
        if period not in period_range:
            raise Exception("Unexpected period: " + period + ". "
                            + "Try to use next - " + str(period_range).strip('[]'))

        if date_from is None:
            date_from = 0

        if date_to is None:
            date_to = 0

        date_format = "%Y-%m" if "month" == period else "%Y-%m-%d"
        if isinstance(date_from, datetime):
            date_from = date_from.strftime(date_format)
        if isinstance(date_to, datetime):
            date_to = date_to.strftime(date_format)

        return self.request("ads.getStatistics", {
            "account_id": account_id,
            "ids_type": ids_type,
            "period": period,
            "ids": ",".join("%s" % int(adv_id) for adv_id in ids),
            "date_from": date_from,
            "date_to": date_to,
        })
