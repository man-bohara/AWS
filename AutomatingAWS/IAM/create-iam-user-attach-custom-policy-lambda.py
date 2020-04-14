import json
import boto3

def lambda_handler(event, context):
    
    iam = boto3.resource('iam')
    
    user = iam.User('sri.bohara')
    
    try:
        user.create(
            Tags= [
                {
                    'Key': 'Owner',
                    'Value': 'man.bohara'
                }
                ]
            )
    except:
        pass
        
    policy = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": [
                        "ec2:*",
                        "s3:*"
                        ],
                    "Resource":"*"
                }]
            }
    policy = iam.create_policy(
            PolicyName= 'ec2-s3-full-access',
            PolicyDocument= json.dumps(policy)
        )
    
    
    user.attach_policy(
            PolicyArn= policy['policy']['Arn']
        )

    user.create_login_profile(
            Password = 'abc123',
            PasswordResetRequired = True
        )
