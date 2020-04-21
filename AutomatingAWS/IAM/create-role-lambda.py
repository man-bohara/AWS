import json, boto3

def lambda_handler(event, context):
    iam_client = boto3.client('iam')
    sts_client = boto3.client('sts')

    role_name = event['RoleName']

    # This following trust policy can be used to provide access to assume this role by a particular IAM user from different AWS acccount
    trust_relationship_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::087851441689:root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # This following trust policy can be used to provide access to assume this role by a particular service in the same account
    # trust_relationship_policy = {
    #     "Version": "2012-10-17",
    #     "Statement": [
    #         {
    #             "Effect": "Allow",
    #             "Principal": {
    #                 "Service": "ec2.amazonaws.com"
    #             },
    #             "Action": "sts:AssumeRole"
    #         }
    #     ]
    # }

    # This following trust policy can be used to provide access to assume this by third party using external
    # trust_relationship_policy = {
    #     "Version": "2012-10-17",
    #     "Statement": {
    #         "Effect": "Allow",
    #         "Action": "sts:AssumeRole",
    #         "Principal": {"AWS": "Example Corp's AWS Account ID"},
    #         "Condition": {"StringEquals": {"sts:ExternalId": "12345"}}
    #     }
    # }

    create_role_res = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_relationship_policy),
        Description='This is a test role',
        Tags=[
            {
                'Key': 'Owner',
                'Value': 'msb'
            }
        ]
    )

    policy_json = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ec2:*"
            ],
            "Resource": "*"
        }]
    }

    policy_name = role_name + '_policy'
    policy_arn = ''
    account_id = sts_client.get_caller_identity()['Account']

    try:
        policy_res = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
        policy_arn = policy_res['Policy']['Arn']
    except:
        policy_arn = 'arn:aws:iam::' + account_id + ':policy/' + policy_name

    policy_attach_res = iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )

    print(create_role_res)
