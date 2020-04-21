import boto3, json


def lambda_handler(event, context):
    iam_client = boto3.client('iam')

    sts = boto3.client('sts')

    user_name = event['UserName']
    policy_name = event['PolicyName']

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
    except:
        return 'User {0} is already available'.format(user_name)

    policy_json = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ec2:*",
                "s3:*"
            ],
            "Resource": "*"
        }]
    }

    policy_arn = ''
    account_id = sts.get_caller_identity()['Account']
    print(account_id)

    try:
        policy = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
        policy_arn = policy['Policy']['Arn']
        print('Policy Arn in try : {0}'.format(policy_arn))
    except:
        policy_arn = 'arn:aws:iam::' + account_id + ':policy/' + policy_name
        print('Policy Arn in except : {0}'.format(policy_arn))

    response = iam_client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )

    print('Final policy arn : {0}'.format(policy_arn))

    print('Attached policy reponse : {0}'.format(response))
    access_secrete_key = iam_client.create_access_key(
        UserName=user_name
    )

    print('User with UserName:{0} got created successfully'.format(user_name))

    access_key = access_secrete_key['AccessKey']['AccessKeyId']
    secret_key = access_secrete_key['AccessKey']['SecretAccessKey']

    ses_client = boto3.client('ses')

    ses_res = ses_client.send_email(
        Source='manmohan.bohara@gmail.com',
        Destination={
            'ToAddresses': [
                'manmohan.bohara@gmail.com'
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
