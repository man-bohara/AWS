import boto3
import json, string, random

def lambda_handler(event, context):
    
    iam_client = boto3.client('iam')
    
    user_name = 'sri.bohara'
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
    except:
        pass
        
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
    account_id = '827178005985'
    policy_name = 'ec2-full-access'
    
    try:
        policy = iam_client.create_policy(
                PolicyName= policy_name,
                PolicyDocument= json.dumps(policy_json)
            )
        policy_arn = policy['Policy']['Arn']
    except:
        policy_arn = 'arn:aws:iam::'+account_id+':policy/'+policy_name
    
    
    response = iam_client.attach_user_policy(
            UserName= user_name,
            PolicyArn= policy_arn
        )
        
    password = randomString()
        
    try:
        login_profile = iam_client.create_login_profile(
                UserName= user_name,
                Password = password,
                PasswordResetRequired = True
            )
    except:
        pass
    
    print('User with UserName:{0} got created successfully'.format(user_name))
    
    return user_name, password
    

def randomString(stringLength=12):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
