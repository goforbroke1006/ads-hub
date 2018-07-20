import json
import os
import sys

from connector.ga_api import get_service, upload_file

key_file_location, acc_id, wp_id, cds_id, imports_dir, backups_dir, = sys.argv[1:]

scope = 'https://www.googleapis.com/auth/analytics'

service = get_service(
    api_name='analytics',
    api_version='v3',
    scopes=[scope],
    key_file_location=key_file_location)

from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(imports_dir) if isfile(join(imports_dir, f))]

all_res = []
for file_name in onlyfiles:
    res = upload_file(service,
                      account_id=acc_id, web_property_id=wp_id,
                      custom_data_source_id=cds_id,
                      file_path=imports_dir + '/' + file_name
                      )
    all_res.append(res)
    os.rename(
        imports_dir + '/' + file_name,
        backups_dir + '/' + file_name
    )

print json.dumps(all_res)
