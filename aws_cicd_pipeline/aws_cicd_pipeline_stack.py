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
from aws_cdk import core
from aws_cicd_pipeline.ecr_build import get_ecr_repo
from aws_cicd_pipeline.load_balancer import get_lb_listener_rule, get_app_lb, get_lb_listener, get_pipeline_tg
from aws_cicd_pipeline.security_group import get_security_group
from aws_cicd_pipeline.cluster_fargate import get_cd_service, cluster_fargate, task_defination
from aws_cicd_pipeline.codedeploy import get_codedeploy, cd_deployment_group



class AwsCicdPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        code_deploy_app = get_codedeploy(self)
        #deployment_group = cd_deployment_group(self, code_deploy_app)
        return
        repo = codecommit.Repository(
            self,
            "Repository",
            repository_name="CodeCommitRepo",
            code=codecommit.Code.from_directory(path.join(".", "source/"), "master"),
            description="Some description")

        ecr_repo = get_ecr_repo(
            self,
            name = "ecr-test"
        )
        #
        pipeline_sg = get_security_group(
            self,
             name = "Pipeline-SecurityGroup"
        )
        
        pipeline_tg = get_pipeline_tg(
             self,
            name = "pipeline_tg"
         )
        #
        app_lb = get_app_lb(
             self,
            name = "app_LB",
            security_group=pipeline_sg
         )
        #
        # lb_Listner = get_lb_listener(
        #     self,
        #     app_lb
        # )
        #
        # lb_listner_rule = get_lb_listener_rule(
        #     self,
        #     pipeline_tg,
        #     lb_Listner
        # )
        ecs_cluster = cluster_fargate(self)

        ecs_taskd = task_defination(self, ecr_repo)

        ecs_service = get_cd_service(self, ecs_cluster, app_lb, pipeline_tg, ecs_taskd)

        codebuild_project = get_cb_project(self, repo, ecr_repo)


        codepipeline.CfnPipeline(self, "CfnPipeline",
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
                                                 configuration={
                                                     "BranchName": "master",
                                                     "RepositoryName": repo.repository_name
                                                 },
                                                 output_artifacts=[
                                                     codepipeline.CfnPipeline.OutputArtifactProperty(
                                                         name="SourceOutput"
                                                     )],
                                                 region="eu-west-1",
                                                 run_order=1
                                             )],
                                         name="Source",
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
                                             configuration={
                                                 "ProjectName": codebuild_project.name,
                                             },
                                             input_artifacts=[codepipeline.CfnPipeline.InputArtifactProperty(
                                                 name="SourceOutput"
                                             )],
                                             output_artifacts=[
                                                 codepipeline.CfnPipeline.OutputArtifactProperty(
                                                     name="BuildOutput"
                                                 )],
                                             region="eu-west-1",
                                             run_order=2
                                         )],
                                         name="CodeBuild",
                                     ),

                                     codepipeline.CfnPipeline.StageDeclarationProperty(
                                         actions=[codepipeline.CfnPipeline.ActionDeclarationProperty(
                                             action_type_id=codepipeline.CfnPipeline.ActionTypeIdProperty(
                                                 category="Deploy",
                                                 owner="AWS",
                                                 provider="Amazon ECS",
                                                 version="1"
                                             ),
                                             name="Deploy",
                                             configuration={
                                                 "CodeDeployName": codeDeploy.application_name,
                                                 "Cluster Name": ecs_cluster.cluster_name,
                                                 "Service Name":ecs_service.service_name,
                                                 #"Image Definitions file": imagedefinitions.json,
                                             },
                                             input_artifacts=[codepipeline.CfnPipeline.InputArtifactProperty(
                                                 name="Build Artifact"
                                             )],
                                             region="eu-west-1",
                                             run_order=3
                                         )],
                                         name="Deploy",
                                     ),
                                     

                                 ],
                                 artifact_store=codepipeline.CfnPipeline.ArtifactStoreProperty(
                                     location="cf-templates-3jcutc9uutje-eu-west-1",
                                     type="S3",
                                 ),
                                 name="CP-1",
                                 )
