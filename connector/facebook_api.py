import requests
from facebook_business.adobjects.adaccount import AdAccount


# from facebookads.objects import Campaign


def some_import_method(camp_id, access_token):
    page_token_url = "https://graph.facebook.com/%s?fields=%s" % (camp_id, access_token)
    res = requests.get(page_token_url, allow_redirects=True)
    print res.text

    ad_account = AdAccount(camp_id)
    fields = [
        # 'campaign_group_name',
        'campaign_name',
        'campaign_id',
        'impressions',
        'clicks',
        'spend',
        'reach',
        'actions',
        'action_values'
    ]
    params = {
        'time_range': {
            'since': '2010-01-01',
            'until': '2018-03-30'
        },
    }
    # print ad_account.get_campaigns()
    print ad_account.get_my_account()
    # ad_insights = ad_account.get_insights(fields=fields, params=params)
    # print ad_insights

    # campaign = Campaign(camp_id)
    # insights = campaign.get_insights()
    # print campaign
    # return campaign
