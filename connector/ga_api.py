from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    """
    Get first analytics profile from all
    :type service: Resource
    :return: ID of default account
    :rtype: str | None
    """

    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:sessions').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print 'View (Profile):', results.get('profileInfo').get('profileName')
        print 'Total Sessions:', results.get('rows')[0][0]

    else:
        print 'No results found'


def upload_file(service, account_id, web_property_id, custom_data_source_id, file_path):
    """
    Upload file with cost data from another sources
    :type service: Resource
    :type account_id: str
    :type web_property_id: str
    :type custom_data_source_id: str
    :return: None
    :rtype: None
    """

    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError

    try:
        media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=False)
        daily_upload = service.management().uploads().uploadData(
            accountId=account_id,
            webPropertyId=web_property_id,
            customDataSourceId=custom_data_source_id,
            media_body=media).execute()
        print daily_upload

    except TypeError, error:
        # Handle errors in constructing a query.
        print 'There was an error in constructing your query : %s' % error

    except HttpError, error:
        # Handle API errors.
        print ('There was an API error : %s : %s' %
               (error.resp.status, error.resp.reason))
