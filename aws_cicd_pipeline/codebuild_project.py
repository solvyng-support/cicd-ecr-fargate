import aws_cdk.aws_codebuild as codebuild
import os
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_ecr as ecr
from aws_cicd_pipeline.codebuild_service_role import get_service_role




def get_cb_project(self, repo: codecommit.IRepository, ecr_repo: ecr.IRepository ):
    return codebuild.CfnProject(self, "MyCfnProject",
                                artifacts=codebuild.CfnProject.ArtifactsProperty(
                                    type="CODEPIPELINE",

                                    # the properties below are optional
                                    # artifact_identifier="artifactIdentifier",
                                    # encryption_disabled=False,
                                    # location="location",
                                    # name="name",
                                    # namespace_type="namespaceType",
                                    # override_artifact_name=False,
                                    # packaging="packaging",
                                    # path="path"
                                ),
                                environment=codebuild.CfnProject.EnvironmentProperty(
                                    compute_type="BUILD_GENERAL1_SMALL",
                                    image="aws/codebuild/standard:4.0",
                                    type="LINUX_CONTAINER",

                                    # the properties below are optional
                                    # certificate="certificate",
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
                                    # image_pull_credentials_type="imagePullCredentialsType",
                                    privileged_mode=True,
                                    # registry_credential=codebuild.CfnProject.RegistryCredentialProperty(
                                    #     credential="credential",
                                    #     credential_provider="credentialProvider"
                                    # )
                                ),
                                service_role="codeBuildServiceRole",
                                source=codebuild.CfnProject.SourceProperty(
                                    type="CODEPIPELINE",

                                    # the properties below are optional
                                    # auth=codebuild.CfnProject.SourceAuthProperty(
                                    #     type="type",
                                    #
                                    #     # the properties below are optional
                                    #     resource="resource"
                                    # ),
                                    build_spec="buildspec.yml",
                                    # build_status_config=codebuild.CfnProject.BuildStatusConfigProperty(
                                    #     context="context",
                                    #     target_url="targetUrl"
                                    # ),
                                    # git_clone_depth=123,
                                    # git_submodules_config=codebuild.CfnProject.GitSubmodulesConfigProperty(
                                    #     fetch_submodules=False
                                    # ),
                                    # insecure_ssl=False,
                                    location=repo.repository_clone_url_http,
                                    # source_identifier="sourceIdentifier"
                                ),

                                # the properties below are optional
                                badge_enabled=False,
                                # build_batch_config=codebuild.CfnProject.ProjectBuildBatchConfigProperty(
                                #     batch_report_mode="batchReportMode",
                                #     combine_artifacts=False,
                                #     restrictions=codebuild.CfnProject.BatchRestrictionsProperty(
                                #         compute_types_allowed=["computeTypesAllowed"],
                                #         maximum_builds_allowed=123
                                #     ),
                                #     service_role="serviceRole",
                                #     timeout_in_mins=123
                                # ),
                                # cache=codebuild.CfnProject.ProjectCacheProperty(
                                #     type="type",
                                #
                                #     # the properties below are optional
                                #     location="location",
                                #     modes=["modes"]
                                # ),
                                # concurrent_build_limit=123,
                                description="description",
                                # encryption_key="encryptionKey",
                                # file_system_locations=[codebuild.CfnProject.ProjectFileSystemLocationProperty(
                                #     identifier="identifier",
                                #     location="location",
                                #     mount_point="mountPoint",
                                #     type="type",
                                #
                                #     # the properties below are optional
                                #     mount_options="mountOptions"
                                # )],
                                logs_config=codebuild.CfnProject.LogsConfigProperty(
                                    cloud_watch_logs=codebuild.CfnProject.CloudWatchLogsConfigProperty(
                                        status="ENABLED",

                                        # the properties below are optional
                                        group_name="cicd-cb-gp",
                                        stream_name="cicd-cd-stream"
                                    ),
                                    # s3_logs=codebuild.CfnProject.S3LogsConfigProperty(
                                    #     status="status",
                                    #
                                    #     # the properties below are optional
                                    #     encryption_disabled=False,
                                    #     location="location"
                                    # )
                                ),
                                name="cb-01",
                                # queued_timeout_in_minutes=123,
                                # resource_access_role="resourceAccessRole",
                                # secondary_artifacts=[codebuild.CfnProject.ArtifactsProperty(
                                #     type="type",
                                #
                                #     # the properties below are optional
                                #     artifact_identifier="artifactIdentifier",
                                #     encryption_disabled=False,
                                #     location="location",
                                #     name="name",
                                #     namespace_type="namespaceType",
                                #     override_artifact_name=False,
                                #     packaging="packaging",
                                #     path="path"
                                # )],
                                # secondary_sources=[codebuild.CfnProject.SourceProperty(
                                #     type="type",
                                #
                                #     # the properties below are optional
                                #     auth=codebuild.CfnProject.SourceAuthProperty(
                                #         type="type",
                                #
                                #         # the properties below are optional
                                #         resource="resource"
                                #     ),
                                #     build_spec="buildSpec",
                                #     build_status_config=codebuild.CfnProject.BuildStatusConfigProperty(
                                #         context="context",
                                #         target_url="targetUrl"
                                #     ),
                                #     git_clone_depth=123,
                                #     git_submodules_config=codebuild.CfnProject.GitSubmodulesConfigProperty(
                                #         fetch_submodules=False
                                #     ),
                                #     insecure_ssl=False,
                                #     location="location",
                                #     report_build_status=False,
                                #     source_identifier="sourceIdentifier"
                                # )],
                                # secondary_source_versions=[codebuild.CfnProject.ProjectSourceVersionProperty(
                                #     source_identifier="sourceIdentifier",
                                #
                                #     # the properties below are optional
                                #     source_version="sourceVersion"
                                # )],
                                # source_version="sourceVersion",
                                # tags=[CfnTag(
                                #     key="key",
                                #     value="value"
                                # )],
                                # timeout_in_minutes=123,
                                # triggers=codebuild.CfnProject.ProjectTriggersProperty(
                                #     build_type="buildType",
                                #     filter_groups=[[codebuild.CfnProject.WebhookFilterProperty(
                                #         pattern="pattern",
                                #         type="type",
                                #
                                #         # the properties below are optional
                                #         exclude_matched_pattern=False
                                #     )]],
                                #     webhook=False
                                # ),
                                # visibility="visibility",
                                # vpc_config=codebuild.CfnProject.VpcConfigProperty(
                                #     security_group_ids=["securityGroupIds"],
                                #     subnets=["subnets"],
                                #     vpc_id="vpcId"
                                # )
                                )
