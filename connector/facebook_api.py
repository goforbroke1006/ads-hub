# from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.business import Business


def some_import_method(camp_id):
    business = Business(camp_id)
    insights = business.get_insights()
    print insights
    return 0

    campaign = Campaign(camp_id)
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
