# IAM Policy Document

## 1. Identity Policies

An I am policy document is list of statements as shown below.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        }
    ]
}

1. Effect - it defines what would be the effect of this statement e.g. Allow or Deny.
2. Action - it defines the API calls e.g. s3:* means all s3 APIs can be called.
3. Resource - 


## 2. Resource Policies
