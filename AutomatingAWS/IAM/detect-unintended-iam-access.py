import json
import boto3
from urllib.request import Request, urlopen
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    print('Received call', event)

    if event['detail']['userIdentity']['type'] != 'IAMUser':
        print('The call is not made by an IAM user')
        return
    else:
        user_name = event['detail']['userIdentity']['userName']
        print('The call is made by an IAM user', user_name)

    iam_client = boto3.client('iam')
    res = iam_client.list_groups_for_user(
        UserName=user_name
    )

    ssm = boto3.client('ssm')
    webhook_url = ssm.get_parameter(
        Name='SlackNotification', WithDecryption=True)

    revoke_json_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyIAMAccess",
                "Effect": "Deny",
                "Action": "iam:*",
                "Resource": "*"
            }
        ]
    }

    sts_client = boto3.client('sts')
    policy_name = 'denyIAMAccess'
    policy_arn = ''
    account_id = sts_client.get_caller_identity()['Account']

    try:
        policy = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(revoke_json_policy)
        )
        policy_arn = policy['Policy']['Arn']
        print('Policy Arn in try : {0}'.format(policy_arn))
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Policy already exists.... hence using the same')
            policy_arn = 'arn:aws:iam::' + account_id + ':policy/' + policy_name
        else:
            print('Unexpected error occurred... cleaning up and exiting from here ')

    is_authrised = False

    for group in res['Groups']:
        if group['GroupName'] == 'Admin':
            is_authrised = True

    if is_authrised == False:

        # Revoke user permission
        try:
            response = iam_client.attach_user_policy(
                UserName=user_name,
                PolicyArn=policy_arn
            )
        except ClientError as error:
            print('Unexpected error occurred while attaching policy. Going ahead to send notification', error)
            pass

        # In case of allowed number of managed policies are attached user, attach inline policy
        try:
            response = iam_client.put_user_policy(
                UserName=user_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(revoke_json_policy)
            )
        except ClientError as error:
            print('Unexpected error occurred while attaching policy. Going ahead to send notification', error)
            pass

        try:
            slack_message = {
                'text': f':fire: Unauthorized user : {user_name}'
            }

            # Send slack notification
            req = Request(webhook_url['Parameter']['Value'],
                          json.dumps(slack_message).encode('utf-8'))
            response = urlopen(req)
            response.read()
        except ClientError as error:
            print("unexpected error occurred", error)
