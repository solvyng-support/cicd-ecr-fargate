import aws_cdk.aws_codedeploy as codedeploy

def get_codedeploy(self):
    return codedeploy.CfnApplication(self, "MyCfnApplication",
    application_name="pipeline-deploy",
    compute_platform="ECS",
)