import boto3, json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    iam_client = boto3.client('iam')

    # sts = boto3.client('sts')

    user_name = event['UserName']
    policy_name = event['PolicyName']
    account_id = event['AccountId']
    sender_email = event['SenderEmail']
    receiver_email = event['ReceiverEmail']

    try:
        user = iam_client.create_user(
            UserName=user_name,
            Tags=[
                {
                    'Key': 'Owner',
                    'Value': 'my-owner'
                }
            ]
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            return 'User {0} is already available'.format(user_name)
        else:
            return 'Unexpected error occurred... User {0} could not be created'.format(user_name)

    policy_json = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowStatement1",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket"
                ],
                "Resource": "arn:aws:s3:::manmohan-videos-bucket",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": ["videos/*"]
                    }
                }
            },
            {
                "Sid": "AllowStatement2",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject"
                ],
                "Resource": "arn:aws:s3:::manmohan-videos-bucket/vidoes/*"
            }
        ]
    }

    policy_arn = ''
    # account_id = sts.get_caller_identity()['Account']
    # print(account_id)

    try:
        policy = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
        policy_arn = policy['Policy']['Arn']
        print('Policy Arn in try : {0}'.format(policy_arn))
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Policy already exists.... hence using the same')
            policy_arn = 'arn:aws:iam::' + account_id + ':policy/' + policy_name
        else:
            print('Unexpected error occurred... cleaning up and exiting from here ')
            iam_client.delete_user(UserName=user_name)
            return error

    try:
        response = iam_client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
    except ClientError as error:
        print('Unexpected error occurred while attaching policy... hence cleaning up', error)
        iam_client.delete_user(UserName=user_name)
        return 'User could not be create', error

    try:
        access_secrete_key = iam_client.create_access_key(
            UserName=user_name
        )
    except ClientError as error:
        print('Unexpected error occurred while creating access key... hence cleaning up')
        iam_client.detach_user_policy(
            UserName= user_name,
            PolicyArn= policy_arn
        )
        iam_client.delete_user(UserName=user_name)
        return 'User could not be create', error

    print('User with UserName:{0} got created successfully'.format(user_name))

    access_key = access_secrete_key['AccessKey']['AccessKeyId']
    secret_key = access_secrete_key['AccessKey']['SecretAccessKey']

    ses_client = boto3.client('ses')

    ses_res = ses_client.send_email(
        Source=sender_email,
        Destination={
            'ToAddresses': [
                receiver_email
            ]
        },
        Message={
            'Subject': {
                'Data': 'Your AWS Access Secret Key'
            },
            'Body': {
                'Text': {
                    'Data': 'Access Key is : "{0}" \nSecrete Key is : "{1}"'.format(access_key, secret_key)
                }
            }
        }
    )
