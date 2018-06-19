from facebook_business import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet


def get_statistics_for_today(camp_id=None):
    if camp_id is None:
        camp_id = FacebookAdsApi.get_default_account_id()

    campaign = Campaign(camp_id)
    params = {
        'date_preset': AdsInsights.DatePreset.today,
    }

    return campaign.get_insights(params=params)


def get_campaigns():
    acc = AdAccount(FacebookAdsApi.get_default_account_id())
    campaigns = acc.get_campaigns(
        fields={
            Campaign.Field.id,
            Campaign.Field.boosted_object_id,
            Campaign.Field.name,
            Campaign.Field.effective_status,
            Campaign.Field.objective,
        }
    )
    # print campaigns

    for camp in campaigns:  # type: Campaign
        # print camp.get_insights(params={
        #     'date_preset': AdsInsights.DatePreset.today,
        # })
        # print camp.get_id_assured()
        ads_list = camp.get_ads(fields={Ad.Field.adset_id, Ad.Field.source_ad, Ad.Field.source_ad_id, Ad.Field.name,
                                   Ad.Field.configured_status, Ad.Field.creative, })
        # print ads

        for ads in ads_list:  # type: Ad
            insights = ads.get_insights(fields=[
                AdsInsights.Field.ad_id,
                AdsInsights.Field.unique_clicks,
                AdsInsights.Field.impressions,
            ], params={
                'level': AdsInsights.Level.ad,
                'date_preset': AdsInsights.DatePreset.last_week_mon_sun,
            })

            print insights


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
