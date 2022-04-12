import aws_cdk.aws_iam as iam


# assume_role_policy_document: Any
# policy_document: Any

def get_service_role(self):
    return iam.CfnRole(self, "CfnPipelineRole",
                       assume_role_policy_document=get_assume_role_doc(self),

                       # the properties below are optional
                       description="description",
                       # managed_policy_arns=["managedPolicyArns"],
                       max_session_duration=3600,
                       # path="path",
                       # permissions_boundary="permissionsBoundary",
                       policies=[iam.CfnRole.PolicyProperty(
                           policy_document=get_policy_doc(self),
                           policy_name="policyName"
                       )],
                       role_name="cfn-codepipeline-role",
                       # tags=[CfnTag(
                       #     key="key",
                       #     value="value"
                       # )]
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
