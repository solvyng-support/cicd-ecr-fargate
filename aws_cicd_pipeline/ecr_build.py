import aws_cdk.aws_ecr as ecr

def get_ecr_repo(self, name):
    return ecr.CfnRepository(self, "CfnRepository",
                             repository_name=name,

                             )
