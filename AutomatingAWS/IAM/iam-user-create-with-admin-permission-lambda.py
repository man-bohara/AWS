import json
import boto3

def lambda_handler(event, context):
    
    iam = boto3.resource('iam')
    
    user = iam.User('k.bohara')
    
    user.create(
        Tags= [
            {
                "Key": "Owner",
                "Value": "man.bohara"
            }
            ]
        )
    
    user.attach_policy(
            PolicyArn= "arn:aws:iam::aws:policy/AdministratorAccess"
        )

    user.create_login_profile(
            Password = 'abc123',
            PasswordResetRequired = True
        )
