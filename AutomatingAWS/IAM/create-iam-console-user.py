import boto3
import json, string, random

from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    # Creating an boto3 client representing IAM service.
    iam_client = boto3.client('iam')
    
    
    # Recieve group and user name as input
    
    group_name = event['GroupName']
    user_name = event['UserName']
    sender_email = event['SenderEmail']
    reciever_email = event['ReceiverEmail']
    account_id = event['AccountId']
    policy_name = event['PolicyName']
    
    try:
        group_response = iam_client.create_group(
            GroupName= group_name)
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Group already exists')
        else:
            print('Unexpected error occured while creating group... exiting from here', error)
            return 'User could not be create', error
        
    try:
        user = iam_client.create_user(
            UserName=user_name,
            Tags= [
                {
                    'Key': 'Owner',
                    'Value': 'ms.bohara'
                }
                ]
            )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('User already exists')
            return 'User already exists'
        else:
            print('Unexpected error occured while creating user.... exiting from here', error)
            return 'User could not be create', error 
        
    policy_json = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": [
                        "ec2:*"
                        ],
                    "Resource":"*"
                }]
            }
    
    policy_arn = ''
    
    try:
        policy = iam_client.create_policy(
                PolicyName= policy_name,
                PolicyDocument= json.dumps(policy_json)
            )
        policy_arn = policy['Policy']['Arn']
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Policy already exists... Hence retreiving policy arn')
            policy_arn = 'arn:aws:iam::'+account_id+':policy/'+policy_name
        else:
            print('Unexpected error occured while creating policy... hence cleaning up', error)
            iam_client.delete_user( UserName= user_name)
            return 'User could not be create', error
    
    try:
        response = iam_client.attach_user_policy(
                UserName= user_name,
                PolicyArn= policy_arn
            )
    except ClientError as error:
        print('Unexpected error occured while attaching policy... hence cleaning up', error)
        iam_client.delete_user( UserName= user_name)
        return 'User could not be create', error
            
    
    password = random_string()
        
    try:
        login_profile = iam_client.create_login_profile(
                UserName= user_name,
                Password = password,
                PasswordResetRequired = True
            )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('login profile already exists')
        else:
            print('Unexpected error occured while creating login profile... hence cleaning up', error)
            return 'User could not be create', error
    
    print('User with UserName:{0} got created successfully'.format(user_name))
    
    # Add user to group
    
    add_user_to_group_res = iam_client.add_user_to_group(
        GroupName= group_name,
        UserName= user_name
        )
    
    # Now user got created... Sending its details via email
    
    ses_client = boto3.client('ses')
    
    ses_res = ses_client.send_email(
        Source= sender_email,
        Destination= {
            'ToAddresses': [
                reciever_email
                ]
        },
        Message= {
            'Subject': {
                'Data': 'You IAM user deatils'
            },
            'Body': {
                'Text': {
                    'Data': 'User name is : "{0}" \nOne time password is : "{1}"'.format(user_name, password)
                }
            }
        }
        )
    
    return 'User with UserName:{0} got created successfully'.format(user_name)
    
# This function generates random string
def random_string(stringLength=12):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
