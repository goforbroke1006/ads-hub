from facebookads.objects import Campaign


def some_import_method(camp_id):
    campaign = Campaign(camp_id)
    insights = campaign.get_insights()
    print insights
    return insights
