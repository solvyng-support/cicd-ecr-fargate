from aws_cdk import (
    core as cdk,
    aws_s3 as s3
)
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codecommit as codecommit
from aws_cicd_pipeline.codebuild_project import get_cb_project
from aws_cicd_pipeline.codepipeline_service_role import get_service_role
from os import name, path
import aws_cdk.aws_codepipeline_actions as codepipeline_actions

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cicd_pipeline.ecr_build import get_ecr_repo
from aws_cicd_pipeline.load_balancer import get_app_LB, get_LB_Listner, get_pipelineTG
from aws_cicd_pipeline.security_group import get_pipelineSG


class AwsCicdPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = codecommit.Repository(
            self,
            "Repository",
            repository_name="MyRepositoryName",
            code=codecommit.Code.from_directory(path.join(".", "source/"), "master"),
            description="Some description")

        ecr_repo = get_ecr_repo(
            self,
            name = "Ecr-test"
        )


        pipelineSG = get_pipelineSG(
            self,
            name = "pipelineSG"
        )

        pipelineTG = get_pipelineTG(
            self,
            name = "pipelineTG"
        )

        LB_Listner = get_LB_Listner(
            self,
            app_LB,
           # name = "LB_Listner"
        )


        app_LB = get_app_LB(
            self,
            pipelineSG,
            pipelineTG,
            name = "app_LB",
            
        )

        codebuild_project = get_cb_project(self, repo, ecr_repo)

        codepipeline.CfnPipeline(self, "MyCfnPipeline",
                                 role_arn=get_service_role(self).attr_arn,
                                 stages=[
                                     codepipeline.CfnPipeline.StageDeclarationProperty(
                                         actions=[
                                             codepipeline.CfnPipeline.ActionDeclarationProperty(
                                                 action_type_id=codepipeline.CfnPipeline.ActionTypeIdProperty(
                                                     category="Source",
                                                     owner="AWS",
                                                     provider="CodeCommit",
                                                     version="1"
                                                 ),
                                                 name="Source",

                                                 # the properties below are optional
                                                 configuration={
                                                     "BranchName": "master",
                                                     "RepositoryName": repo.repository_name
                                                 },
                                                 # input_artifacts=[codepipeline.CfnPipeline.InputArtifactProperty(
                                                 #     name="name"
                                                 # )],
                                                 # namespace="namespace",
                                                 output_artifacts=[
                                                     codepipeline.CfnPipeline.OutputArtifactProperty(
                                                         name="SourceOutput"
                                                     )],
                                                 region="eu-west-1",
                                                 # role_arn="roleArn",
                                                 run_order=1
                                             )],
                                         name="Source",

                                         # the properties below are optional
                                         # blockers=[codepipeline.CfnPipeline.BlockerDeclarationProperty(
                                         #     name="name",
                                         #     type="type"
                                         # )]
                                     ),

                                     codepipeline.CfnPipeline.StageDeclarationProperty(
                                         actions=[codepipeline.CfnPipeline.ActionDeclarationProperty(
                                             action_type_id=codepipeline.CfnPipeline.ActionTypeIdProperty(
                                                 category="Build",
                                                 owner="AWS",
                                                 provider="CodeBuild",
                                                 version="1"
                                             ),
                                             name="Build",

                                             # the properties below are optional
                                             configuration={
                                                 "ProjectName": codebuild_project.name,
                                             },
                                             input_artifacts=[codepipeline.CfnPipeline.InputArtifactProperty(
                                                 name="SourceOutput"
                                             )],
                                             # namespace="namespace",
                                             output_artifacts=[
                                                 codepipeline.CfnPipeline.OutputArtifactProperty(
                                                     name="BuildOutput"
                                                 )],
                                             region="eu-west-1",
                                             # role_arn="roleArn",
                                             run_order=2
                                         )],
                                         name="CodeBuild",

                                         # the properties below are optional
                                         # blockers=[codepipeline.CfnPipeline.BlockerDeclarationProperty(
                                         #     name="name",
                                         #     type="type"
                                         # )]
                                     ),

                                 ],

                                 # the properties below are optional
                                 artifact_store=codepipeline.CfnPipeline.ArtifactStoreProperty(
                                     location="cf-templates-3jcutc9uutje-eu-west-1",
                                     type="S3",

                                     # the properties below are optional
                                     # encryption_key=codepipeline.CfnPipeline.EncryptionKeyProperty(
                                     #     id="id",
                                     #     type="type"
                                     # )
                                 ),
                                 # artifact_stores=[codepipeline.CfnPipeline.ArtifactStoreMapProperty(
                                 #     artifact_store=codepipeline.CfnPipeline.ArtifactStoreProperty(
                                 #         location="location",
                                 #         type="type",
                                 #
                                 #         # the properties below are optional
                                 #         encryption_key=codepipeline.CfnPipeline.EncryptionKeyProperty(
                                 #             id="id",
                                 #             type="type"
                                 #         )
                                 #     ),
                                 #     region="region"
                                 # )],
                                 # disable_inbound_stage_transitions=[
                                 #     codepipeline.CfnPipeline.StageTransitionProperty(
                                 #         reason="reason",
                                 #         stage_name="stageName"
                                 #     )],
                                 name="CP-1",
                                 # restart_execution_on_update=False,
                                 # tags=[CfnTag(
                                 #     key="key",
                                 #     value="value"
                                 # )]
                                 )
