import sys

from connector.ga_api import get_service, upload_file

key_file_location, acc_id, wp_id, cds_id, fp, = sys.argv[1:]

scope = 'https://www.googleapis.com/auth/analytics'

service = get_service(
    api_name='analytics',
    api_version='v3',
    scopes=[scope],
    key_file_location=key_file_location)

upload_file(service,
            account_id=acc_id, web_property_id=wp_id,
            custom_data_source_id=cds_id,
            file_path=fp
            )
