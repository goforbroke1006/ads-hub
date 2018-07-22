import csv


class CsvExportWriter:

    def __init__(self, target_directory, provider_name, date):
        self.provider_name = provider_name
        self.date = date

        self.file_path = '%s/%s-%s.csv' % (target_directory, provider_name, date)
        self.file_stream = open(self.file_path, 'wb')
        self.writer = csv.writer(self.file_stream, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow([
            'ga:source', 'ga:medium', 'ga:campaign', 'ga:adwordsCampaignID',
            'ga:keyword', 'ga:adContent',
            'ga:adCost', 'ga:adClicks', 'ga:impressions',
            'ga:adGroup', 'ga:adSlot', 'ga:date', 'ga:importBehavior',
        ])
        self.file_stream.flush()

    def write(self, ga_medium, ga_campaign, ga_adwards_campaign_id,
              ga_keyword, ga_ad_content,
              ga_ad_cost, ga_ad_clicks, ga_impressions,
              ga_ad_group, ga_ad_slot, ga_date,
              ga_import_behavior):

        if ga_adwards_campaign_id is None:
            ga_adwards_campaign_id = '(not set)'

        if ga_keyword is None:
            ga_keyword = '(not set)'

        if ga_ad_content is None:
            ga_ad_content = '(not set)'

        ga_ad_cost = int(round(float(ga_ad_cost)))
        ga_ad_clicks = int(round(float(ga_ad_clicks)))
        ga_impressions = int(round(float(ga_impressions)))

        ga_date = ga_date.strftime('%Y%m%d')

        if ga_ad_group is None:
            ga_ad_group = '(not set)'

        if ga_ad_slot is None:
            ga_ad_slot = 0

        if ga_import_behavior is None:
            ga_import_behavior = 'SUMMATION'

        self.writer.writerow([
            self.provider_name,
            ga_medium,
            ga_campaign,
            ga_adwards_campaign_id,
            ga_keyword,
            ga_ad_content,

            ga_ad_cost,
            ga_ad_clicks,
            ga_impressions,

            ga_ad_group,
            ga_ad_slot,
            ga_date,
            ga_import_behavior,
        ])
        self.file_stream.flush()
