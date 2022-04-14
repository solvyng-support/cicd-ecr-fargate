import aws_cdk.aws_codedeploy as codedeploy

def get_codedeploy(self):
    return codedeploy.CfnApplication(self, "CfnApplication",
    application_name="pipeline-deploy",
    compute_platform="ECS",
)

def cd_deployment_group(self, app:codedeploy.CfnApplication ):
    dg =  codedeploy.CfnDeploymentGroup(self, "CfnDeploymentGroup",
        application_name=app.application_name,
        service_role_arn="arn:aws:iam::456561060854:role/cdk-codedepoly",
        deployment_group_name="CfnDeploymentGroup",
        # ecs_services=[codedeploy.CfnDeploymentGroup.ECSServiceProperty(
        #     cluster_name="clusterName",
        #     service_name="serviceName"
        # )],
        # load_balancer_info=codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty(
        #     elb_info_list=[codedeploy.CfnDeploymentGroup.ELBInfoProperty(
        #         name="name"
        #     )],
        #     target_group_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
        #         name="name"
        #     )],
        #     target_group_pair_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty(
        #         prod_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
        #             listener_arns=["listenerArns"]
        #         ),
        #         target_groups=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
        #             name="name"
        #         )],
        #         test_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
        #             listener_arns=["listenerArns"]
        #         )
        #     )]
        # ),
    )

    dg.add_depends_on(target=app)
    return dg


