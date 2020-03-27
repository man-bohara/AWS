# IAM Policy Document

## 1. Identity Policies

Identiy policy is attached to IAM users. An identity policy document is list of statements and each statement has following elements.

1. Effect - It defines what would be the effect of this statement e.g. Allow or Deny.
2. Action - It defines which API calls the user can make e.g. "s3:*" => means user can call all s3 APIs.
3. Resource - It defines which AWS resources the user can access e.g. "arn:aws:s3:::<my_bucket>" => means user can only access my_bucket.
4. Condition - We can have additional conditions which must satisfy to make this statement take effect.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::<my_bucket>"
        }
    ]
}

## 2. Resource Policies

Resource policies are quit similar to identity polices only difference is that it needs an additional element called Principal and These policies are attached to resources.
The Principal defines which identity/user, this policy applies to. In identity policy, Principal is preasumed the user to which the policy is attached.
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": *,
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::<my_bucket>"
        }
    ]
}

