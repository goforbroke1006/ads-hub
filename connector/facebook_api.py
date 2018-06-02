from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet


def some_import_method(camp_id):
    # account = AdAccount('act_%s' % camp_id)
    # adsets = account.get_ad_sets(fields=[AdSet.Field.name])
    #
    # for adset in adsets:
    #     print(adset[AdSet.Field.name])
    #
    # return 0

    # business = Business(camp_id)
    # insights = business.get_insights()
    # print insights
    # return 0

    campaign = Campaign(23842910504540140)
    params = {
        'date_preset': "last_7_days",
    }
    insights = campaign.get_insights(params)
    print insights
    return 0

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
    print ad_account.get_campaigns()
    print ad_account.get_my_account()
    ad_insights = ad_account.get_insights(fields=fields, params=params)
    print ad_insights

    # campaign = Campaign(camp_id)
    # insights = campaign.get_insights()
    # print campaign
    # return campaign
