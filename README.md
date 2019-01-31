# Former
CloudFormation supports lots of different AWS Resources with many parameters. Remembering all of them is a pain
and slows down development dramatically.

To make this faster `Former` lets you create a full CF resource example for any supported Resource. It parses
the [CloudFormation Resource Specification](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html)
to get the definition for all resources.

## Example

You can create an example for any aws resource by calling former with the service and resource name. In the following
 example we're creating an `AWS::IAM::User` Resource:

```bash
root@e41871e1eb3e:/app# former iam user
Resources:
  AWSIAMUser:
    Parameters:
      Groups:
      - String
      LoginProfile:
        Password: String - Required
        PasswordResetRequired: Boolean
      ManagedPolicyArns:
      - String
      Path: String
      Policies:
      - PolicyDocument: Json - Required
        PolicyName: String - Required
      UserName: String
    Type: AWS::IAM::User
```

Some Resources also have a subtype (e.g. LoginProfile for the IAM::User). If you only want to show the subtype
you can add it as a third parameter:

```bash
root@e41871e1eb3e:/app# former iam user loginprofile
Resources:
  AWSIAMUserLoginProfile:
    Parameters:
      Password: String - Required
      PasswordResetRequired: Boolean
    Type: AWS::IAM::User.LoginProfile
```

Of course this is not valid CloudFormation as the `LoginProfile` is not a valid CF Resource. But it helps when you 
want to get a quick overview for a subtype.

## Options

* `--json` Print output in json instead of yaml
* `--docs` Open the AWS docs to the resource specified