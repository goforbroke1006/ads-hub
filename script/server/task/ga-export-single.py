import json
import os
import sys

import connector

key_file_location, acc_id, wp_id, cds_id, imports_file, backups_dir, = sys.argv[1:]
imports_file = os.path.abspath(imports_file)
file_name = os.path.basename(imports_file)

scope = 'https://www.googleapis.com/auth/analytics'
service = connector.ga_api.get_service(
    api_name='analytics',
    api_version='v3',
    scopes=[scope],
    key_file_location=key_file_location)

res = connector.ga_api.upload_file(service,
                                   account_id=acc_id, web_property_id=wp_id,
                                   custom_data_source_id=cds_id,
                                   file_path=imports_file
                                   )
os.remove(imports_file)
print json.dumps(res)
