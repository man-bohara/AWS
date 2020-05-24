import json
import boto3
import datetime
from botocore.exceptions import ClientError

list_users_to_remove = []
list_access_keys_to_remove = []
date_now = datetime.datetime.now()
iam_client = boto3.client('iam')
max_idle_days = 90

def lambda_handler(event, context):

    max = event['MaxItems']

    try:
        res_users = iam_client.list_users(
            MaxItems=max
        )
        check_credentials(res_users)
    except ClientError as error:
        pass

    if res_users['IsTruncated']:
        while res_users['IsTruncated']:
            marker = res_users['Marker']
            res_users = iam_client.list_users(
                Marker=marker,
                MaxItems=max
            )

            check_credentials(res_users)

    for user_name in list_users_to_remove:
        print('User {0} needs to be removed'.format(user_name))

    for access_key in list_access_keys_to_remove:
        print('Access kye {0} needs to be removed'.format(access_key))

    return list_users_to_remove, list_access_keys_to_remove


def check_credentials(res_users):
    created_date = datetime.datetime.now()
    last_used_date = datetime.datetime.now()
    access_key_id = None

    for user in res_users['Users']:
        if 'PasswordLastUsed' in user: # Checking for console user password last usage
            last_used_date = user['PasswordLastUsed'].replace(tzinfo=None)

            difference = date_now - last_used_date

            if difference.days > max_idle_days:
                list_users_to_remove.append(user['UserName'])

        # Below we are checking for access keys last usage
        res_keys = iam_client.list_access_keys(
            UserName=user['UserName'],
            MaxItems=5)

        if 'AccessKeyMetadata' in res_keys:
            for key in res_keys['AccessKeyMetadata']:
                if 'CreateDate' in key:
                    created_date = res_keys['AccessKeyMetadata'][0]['CreateDate'].replace(tzinfo=None)
                if 'AccessKeyId' in key:
                    access_key_id = key['AccessKeyId']
                    res_last_used_key = iam_client.get_access_key_last_used(
                        AccessKeyId=access_key_id)
                    if 'LastUsedDate' in key:
                        last_used_date = res_last_used_key['AccessKeyLastUsed']['LastUsedDate'].replace(tzinfo=None)
                    else:
                        last_used_date = created_date

        difference = date_now - last_used_date

        if difference.days > max_idle_days:
            list_access_keys_to_remove.append(access_key_id)
