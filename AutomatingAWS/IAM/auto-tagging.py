import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    print('Received event : ', event)

    cw_event = json.loads(event['Records'][0]['Sns']['Message'])

    print('Event after conversion from SNS : ', cw_event)

    region = cw_event['region']
    account = cw_event['account']
    creator = cw_event['detail']['userIdentity']['principalId']

    instance_arn = get_arn(cw_event)

    sts_client = boto3.client('sts')

    try:
        sts_response = sts_client.assume_role(
            RoleArn='arn:aws:iam::087851441689:role/AdminRoleForAssuming',
            RoleSessionName='assume_role_session'
        )
    except ClientError as error:
        print('Unexpected error occurred... could not assume role', error)
        return error

    rg_client = boto3.client('resourcegroupstaggingapi',
                             region,
                             aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                             aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                             aws_session_token=sts_response['Credentials']['SessionToken'])

    print('creating tag for instance {}'.format(instance_arn))

    try:
        print('instance arn is ', instance_arn)
        response = rg_client.tag_resources(
            ResourceARNList=[
                instance_arn,
            ],
            Tags={
                'Creator': creator,
                'Owner': account
            }
        )
        print('tag got created')
    except ClientError as error:
        print(error)


def get_arn(event):
    instance_arn = ''
    source = event['source']
    region = event['region']
    account = event['account']

    print('Source is :', source)
    print('Region is :', region)
    print('Account is :', account)

    if source == 'aws.ec2':
        event_name = event['detail']['eventName']
        if event_name == 'RunInstances':
            instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
            ec2_client = boto3.client('ec2')
            waiter = ec2_client.get_waiter('instance_exists')
            waiter.wait(
                InstanceIds=[
                    instance_id,
                ]
            )
            instance_arn = 'arn:aws:ec2:' + region + ':' + account + ':instance/' + instance_id

    if source == 'aws.lambda':
        event_name = event['detail']['eventName']
        print('Event name :', event_name)
        if event_name == 'CreateFunction20150331':
            function_name = event['detail']['responseElements']['functionName']
            print('Functin name :', function_name)
            try:
                lambda_client = boto3.client('lambda')
                waiter = lambda_client.get_waiter('function_exists')

                waiter.wait(
                    FunctionName=function_name,
                    WaiterConfig={
                        'Delay': 123,
                        'MaxAttempts': 123
                    }
                )
            except ClientError as error:
                print(error)
            print('Before Instance ARN: ', function_name)
            instance_arn = event['detail']['responseElements']['functionArn']
            print('After Instance ARN, ', instance_arn)

    if source == 'aws.rds':
        event_name = event['detail']['eventName']
        if event_name == 'CreateDBInstance':
            db_instance_id = event['detail']['requestParameters']['dBInstanceIdentifier']
            rds_client = boto3.client('rds')
            waiter = rds_client.get_waiter('db_instance_available')
            waiter.wait(
                DBInstanceIdentifier=db_instance_id
            )

            instance_arn = event['detail']['responseElements']['dBInstanceArn']

    if source == 'aws.s3':
        event_name = event['detail']['eventName']
        if event_name == 'CreateBucket':
            bucket_name = event['detail']['requestParameters']['bucketName']
            s3_client = boto3.client('s3')
            waiter = s3_client.get_waiter('bucket_exists')
            waiter.wait(
                Bucket=bucket_name,
                WaiterConfig={
                    'Delay': 123,
                    'MaxAttempts': 123
                }
            )
            instance_arn = 'arn:aws:s3:::' + bucket_name

    if source == 'aws.dynamodb':
        event_name = event['detail']['eventName']
        if event_name == 'CreateTable':
            table_name = event['detail']['responseElements']['tableDescription']['tableName']
            dd_client = boto3.client('dynamodb')
            waiter = dd_client.get_waiter('table_exists')
            waiter.wait(
                TableName=table_name,
                WaiterConfig={
                    'Delay': 123,
                    'MaxAttempts': 123
                }
            )
            instance_arn = event['detail']['responseElements']['tableDescription']['tableArn']

    return instance_arn
