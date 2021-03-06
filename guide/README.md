# User Guide

## How to setup GA export script

1. Create account in https://analytics.google.com/
2. Open administrator's panel via button with gear icon in left menu
3. Click on breadcrumbs in left-top corner of page to see **account_id** and **web_property_id**

    ![Account ID and web property ID location](ga-account-id-location.png)

4. Click on "Data import" button in resource's section (center section between "account" and "view")
5. Create new data-set
6. Copy **custom_data_source_id** which will have been generated for you data-set

    ![Custom data source ID location](ga-custom-data-source-id-location.png)

7. Create project in https://console.developers.google.com/
8. In "credentials" section create service account
9. Save key file to local machine. Use this file as **key_file_location** property

9. Use this values for GA export

```bash
$ python2.7 ./script/server/task/ga-export.py <key_file_location> \
    <account_id> <web_property_id> <custom_data_source_id> \
    <your_file_with_GA_data>
```
