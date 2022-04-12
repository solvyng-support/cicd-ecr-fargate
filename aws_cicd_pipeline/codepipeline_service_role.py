import aws_cdk.aws_iam as iam

def get_service_role(self):
    return iam.CfnRole(self, "CfnPipelineRole",
                       assume_role_policy_document=get_assume_role_doc(self),
                       description="description",
                       max_session_duration=3600,
                       policies=[iam.CfnRole.PolicyProperty(
                           policy_document=get_policy_doc(self),
                           policy_name="policyName"
                       )],
                       role_name="cfn-codepipeline-role",
                       )


def get_assume_role_doc(self):
    return iam.PolicyDocument.from_json({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "codepipeline.amazonaws.com"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })


def get_policy_doc(self):
    return iam.PolicyDocument(
        statements=[iam.PolicyStatement(
            actions=["s3:*"],
            resources=["*"]
        ),
            iam.PolicyStatement(
                actions=["ecr:*"],
                resources=["*"]
            ),
            iam.PolicyStatement(
                actions=["codecommit:*"],
                resources=["*"]
            ),
            iam.PolicyStatement(
                actions=["codebuild:*"],
                resources=["*"]
            ),
            iam.PolicyStatement(
                actions=["codedeploy:*"],
                resources=["*"]
            )
        ]
    )
