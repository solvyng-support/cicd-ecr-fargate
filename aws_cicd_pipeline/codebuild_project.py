import aws_cdk.aws_codebuild as codebuild
import os
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_ecr as ecr
from aws_cicd_pipeline.codebuild_service_role import get_service_role


def get_cb_project(self, repo: codecommit.IRepository, ecr_repo: ecr.IRepository):
    return codebuild.CfnProject(self, "CfnProject",
                                artifacts=codebuild.CfnProject.ArtifactsProperty(
                                    type="CODEPIPELINE",
                                ),
                                environment=codebuild.CfnProject.EnvironmentProperty(
                                    compute_type="BUILD_GENERAL1_SMALL",
                                    image="aws/codebuild/standard:4.0",
                                    type="LINUX_CONTAINER",
                                    environment_variables=[codebuild.CfnProject.EnvironmentVariableProperty(
                                        name="AWS_DEFAULT_REGION",
                                        value=os.getenv('CDK_DEFAULT_REGION'),
                                        type="PLAINTEXT"
                                    ),
                                        codebuild.CfnProject.EnvironmentVariableProperty(
                                            name="AWS_ACCOUNT_ID",
                                            value=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                            type="PLAINTEXT"
                                        ),
                                        codebuild.CfnProject.EnvironmentVariableProperty(
                                            name="IMAGE_TAG",
                                            value="1.0.0",
                                            type="PLAINTEXT"
                                        ),
                                        codebuild.CfnProject.EnvironmentVariableProperty(
                                            name="IMAGE_REPO_NAME",
                                            value=ecr_repo.repository_name,
                                            type="PLAINTEXT"
                                        )
                                    ],
                                    privileged_mode=True,
                                ),
                                service_role="codeBuildServiceRole",
                                source=codebuild.CfnProject.SourceProperty(
                                    type="CODEPIPELINE",
                                    build_spec="buildspec.yml",
                                    location=repo.repository_clone_url_http,
                                ),
                                badge_enabled=False,
                                description="description",
                                logs_config=codebuild.CfnProject.LogsConfigProperty(
                                    cloud_watch_logs=codebuild.CfnProject.CloudWatchLogsConfigProperty(
                                        status="ENABLED",
                                        group_name="cicd-cb-gp",
                                        stream_name="cicd-cd-stream"
                                    ),
                                ),
                                name="cb-01",
                                )
