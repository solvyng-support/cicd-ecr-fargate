# The code below shows an example of how to instantiate this type.
# The values are placeholders you should change.

from multiprocessing.dummy.connection import Listener
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
from aws_cicd_pipeline.load_balancer import get_app_lb, get_pipeline_tg
from aws_cicd_pipeline.ecr_build import get_ecr_repo


def cluster_fargate(self):
    return ecs.CfnCluster(self, "MyCfnCluster",
        capacity_providers=["FARGATE"],
        cluster_name="allthecatapps",

    )
    
    #Task Defination
#def fargate_service(self, task_d: ecs.TaskDefinition, cluster_f: ecs.CfnCluster, alb: elbv2.CfnLoadBalancer, alb_listener: elbv2.CfnListener ):
   # return ecs.FargateService(self, "Service", cluster=cluster_f, task_definition=task_d, lb=alb, lb_listener=alb_listener)


def task_defination(self, get_ecr_repo:ecr.CfnRepository):    
    return ecs.CfnTaskDefinition(self, "CfnTaskDefinition",
        container_definitions=[ecs.CfnTaskDefinition.ContainerDefinitionProperty( 
            depends_on=[ecs.CfnTaskDefinition.ContainerDependencyProperty(
                container_name="catpipeline"  
            )],
            image=get_ecr_repo.attr_repository_uri,
            port_mappings=[ecs.CfnTaskDefinition.PortMappingProperty(
                container_port=80,
                protocol="tcp"
            )],
        )],
        cpu="0.5vCPU",
        #name="catpipelinedemo",
        execution_role_arn="arn:aws:iam::456561060854:role/taskExecutionRole",
        family="linux",
        memory="1024",
    
)

def get_cd_service(self, cluster_fargate:ecs.CfnCluster, get_app_lb:elbv2.CfnLoadBalancer, get_pipeline_tg:elbv2.CfnTargetGroup, task_defination:ecs.CfnTaskDefinition):
    return ecs.CfnService(self, "CfnService",
        capacity_provider_strategy=[ecs.CfnService.CapacityProviderStrategyItemProperty(
            base=1,
            capacity_provider="FARGATE",
            weight=1
        )],
        cluster=cluster_fargate.attr_arn,
        deployment_controller=ecs.CfnService.DeploymentControllerProperty(
            type="ECS"
        ),
        desired_count=2,
        launch_type="FARGATE",
        load_balancers=[ecs.CfnService.LoadBalancerProperty(
            container_port=80,
            container_name="catpipeline",
            load_balancer_name=get_app_lb.attr_load_balancer_name,
            target_group_arn=get_pipeline_tg.attr_target_group_full_name
        )],
        #network_configuration=ecs.CfnService.NetworkConfigurationProperty(
          #  awsvpc_configuration=ecs.CfnService.AwsVpcConfigurationProperty(
           #     subnets="",
           #     assign_public_ip="ENABLED",
           # )
        #),
        role="arn:aws:iam::456561060854:role/taskExecutionRole",
        service_name="ecs_service",
        task_definition=task_defination.attr_task_definition_arn
    )

 