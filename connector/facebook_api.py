from facebookads.objects import Campaign

def some_import_method():
    campaign = Campaign('hello')
    insights = campaign.get_insights()
    print insights
    return insights