from facebook_business import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign


def get_statistics_for_today(camp_id=None):
    if camp_id is None:
        camp_id = FacebookAdsApi.get_default_account_id()

    campaign = Campaign(camp_id)
    params = {
        'date_preset': AdsInsights.DatePreset.today,
    }

    return campaign.get_insights(params=params)


def get_campaigns():
    """
    Get all ads
    :return: :class:`list of Campaign`
    :rtype: list of Campaign
    """

    acc = AdAccount(FacebookAdsApi.get_default_account_id())
    return acc.get_campaigns(
        params={
            Campaign.Field.effective_status: [
                Campaign.ConfiguredStatus.active,
                Campaign.ConfiguredStatus.paused,
            ],
        },
        fields={
            Campaign.Field.id,
            Campaign.Field.boosted_object_id,
            Campaign.Field.name,
            Campaign.Field.start_time,
            Campaign.Field.stop_time,
            Campaign.Field.effective_status,
            Campaign.Field.objective,
            Campaign.Field.adlabels,
        }
    )


def get_ads(campaign):
    """
    Get all ads
    :type campaign: Campaign
    :return: :class:`list of Ad`
    :rtype: list of Ad
    """
    return campaign.get_ads(
        fields={
            # Ad.Field.name,
            # Ad.Field.status,

            Ad.Field.account_id,
            Ad.Field.ad_review_feedback,
            Ad.Field.adlabels,
            Ad.Field.adset,
            Ad.Field.adset_id,
            Ad.Field.bid_amount,
            Ad.Field.bid_info,
            Ad.Field.bid_type,
            Ad.Field.campaign,
            Ad.Field.campaign_id,
            Ad.Field.configured_status,
            Ad.Field.conversion_specs,
            Ad.Field.created_time,
            Ad.Field.creative,
            Ad.Field.effective_status,
            Ad.Field.id,
            Ad.Field.last_updated_by_app_id,
            Ad.Field.name,
            Ad.Field.recommendations,
            Ad.Field.source_ad,
            Ad.Field.source_ad_id,
            Ad.Field.status,
            Ad.Field.tracking_specs,
            Ad.Field.updated_time,
            Ad.Field.adset_spec,
            Ad.Field.date_format,
            Ad.Field.display_sequence,
            Ad.Field.execution_options,
            Ad.Field.filename,
        }
    )


def get_insights(ad):
    """
    Get insight for advertising
    :type ad: Ad
    :return: :class:`list of AdsInsights`
    :rtype: list of AdsInsights
    """

    return ad.get_insights(fields=[
        AdsInsights.Field.ad_id,
        AdsInsights.Field.unique_clicks,
        AdsInsights.Field.impressions,
        AdsInsights.Field.spend,

        AdsInsights.Field.cpc,
        AdsInsights.Field.cpm,
        AdsInsights.Field.cpp,
        AdsInsights.Field.ctr,
    ], params={
        'level': AdsInsights.Level.ad,
        'date_preset': AdsInsights.DatePreset.yesterday,
    })
