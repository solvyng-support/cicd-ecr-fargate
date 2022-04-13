# The code below shows an example of how to instantiate this type.
# The values are placeholders you should change.

from multiprocessing.dummy.connection import Listener
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_elasticloadbalancingv2 as elbv2


def cluster_fargete(self):
    return ecs.CfnCluster(self, "MyCfnCluster",
        capacity_providers=["FARGATE"],
        cluster_name="allthecatapps",

    )
    
    #Task Defination
def fargate_service(self, task_d: ecs.TaskDefinition, cluster_f: ecs.CfnCluster, alb: elbv2.CfnLoadBalancer, alb_listener: elbv2.CfnListener ):
    return ecs.FargateService(self, "Service", cluster=cluster_f, task_definition=task_d, lb=alb, lb_listener=alb_listener)


def task_defination(self, ecr: ecr.Repository):    
    return ecs.CfnTaskDefinition(self, "CfnTaskDefinition",
        container_definitions=[ecs.CfnTaskDefinition.ContainerDefinitionProperty( 
            depends_on=[ecs.CfnTaskDefinition.ContainerDependencyProperty(
                container_name="catpipeline"  
            )],
            image=ecr.repository_uri,
            port_mappings=[ecs.CfnTaskDefinition.PortMappingProperty(
                container_port=80,
                protocol="tcp"
            )],
        )],
        cpu="0.5vCPU",
        name="catpipelinedemo",
        execution_role_arn="arn:aws:iam::456561060854:role/taskExecutionRole",
        family="linux",
        memory="1024",
    
)

 