import aws_cdk.aws_ecr as ecr


# repository_policy_text: Any
def get_ecr_repo(self, name):
    return ecr.CfnRepository(self, "MyCfnRepository",
                             # encryption_configuration=ecr.CfnRepository.EncryptionConfigurationProperty(
                             #   encryption_type="encryptionType",
                             #
                             #   ),
                             #  image_scanning_configuration=ecr.CfnRepository.ImageScanningConfigurationProperty(
                             #     scan_on_push=False
                             # ),
                             # image_tag_mutability="imageTagMutability",
                             # lifecycle_policy=ecr.CfnRepository.LifecyclePolicyProperty(
                             # lifecycle_policy_text="lifecyclePolicyText",
                             # registry_id="registryId"
                             # ),
                             repository_name=name,

                             )
