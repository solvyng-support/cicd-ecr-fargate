import aws_cdk.aws_ecr as ecr


# repository_policy_text: Any
def get_ecr_repo(self, name):
    return ecr.CfnRepository(self, "CfnRepository",
                             repository_name=name,

                             )
