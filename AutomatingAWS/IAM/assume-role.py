import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    sts_client = boto3.client('sts')

    try:
        response = sts_client.assume_role(
            RoleArn='arn:aws:iam::<TRUSTING_ACCOUNT_ID>:role/<ROLE_NAME_IN_TRUSTING_ACCOUNT>',
            RoleSessionName='assume_role_session'
        )
    except ClientError as error:
        print('Unexpected error occurred... could not assume role', error)
        return error

    try:
        iam_client = boto3.client('iam',
                                  aws_access_key_id=response['Credentials']['AccessKeyId'],
                                  aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                  aws_session_token=response['Credentials']['SessionToken']
                                  )
    except ClientError as error:
        print('Unexpected error occurred... could not create iam client on trusting account', error)
        return error

    user_name = event['UserName']
    try:
        res = iam_client.list_groups_for_user(
            UserName=user_name
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchEntityException':
            print('There is no user with name {0}'.format(user_name))
            return error
        else:
            print('Unexpected error occurred... exiting from here', error)
            return error

    for group in res['Groups']:
        print(group['GroupName'])
