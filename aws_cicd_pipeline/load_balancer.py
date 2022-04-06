import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_ec2 as ec2
import os

from aws_cdk.core import Arn


def get_app_LB(self, pipelineSG: ec2.ISecurityGroup, pipelineTG: elbv2.ITargetGroup, name  ):
    return elbv2.CfnLoadBalancer(self, "MyCfnLoadBalancer",
    ip_address_type="ipv4",
    load_balancer_attributes=[elbv2.CfnLoadBalancer.LoadBalancerAttributeProperty(
        key="TargetGroup",
        value=pipelineTG.target_group_name,
       
    )],
    name= name,
    #scheme="scheme",
    security_groups= pipelineSG.security_group_id,
    subnet_mappings=[elbv2.CfnLoadBalancer.SubnetMappingProperty(
        subnet_id="subnet-013cf74ac52dd1b6b", 
        # the properties below are optional
        #allocation_id="allocationId",
        #i_pv6_address="iPv6Address",
        #private_iPv4_address="privateIPv4Address"
    )],
  
    #tags=[CfnTag(
        #key="key",
        #value="value"
    #)],
    type="application"
)


#### Listner


def get_LB_Listner(self, app_LB: elbv2.ILoadBalancerV2 ):
    return elbv2.CfnListener(self, "MyCfnListener",
    load_balancer_arn=get_app_LB(self).getattr(id),
    # the properties below are optional
    #alpn_policy=["alpnPolicy"],
    #certificates=[elbv2.CfnListener.CertificateProperty(
        #certificate_arn="certificateArn"
    #)],
    port=80,
    protocol="tcp",
    #ssl_policy="sslPolicy"
)


### Target Group

def get_pipelineTG(self, name):
    return elbv2.CfnTargetGroup(self, "MyCfnTargetGroup",
    #health_check_enabled=False,
    #health_check_interval_seconds=123,
    #health_check_path="healthCheckPath",
    #health_check_port="healthCheckPort",
    #health_check_protocol="healthCheckProtocol",
    #health_check_timeout_seconds=123,
    #healthy_threshold_count=123,
    ip_address_type="ipv4",
    #matcher=elbv2.CfnTargetGroup.MatcherProperty(
        #grpc_code="grpcCode",
        #http_code="httpCode"
    #),
    target_group_name=name,
    port=80,
    protocol="tcp",
    protocol_version="HTTP1",
    #tags=[CfnTag(
        #key="key",
        #value="value"
    #)],
    #target_group_attributes=[elbv2.CfnTargetGroup.TargetGroupAttributeProperty(
        #key="key",
        #value="value"
    #)],
    #targets=[elbv2.CfnTargetGroup.TargetDescriptionProperty(
        #id="id",

        # the properties below are optional
        #availability_zone="availabilityZone",
        #port=123
    #)],
    target_type="ip",
    #unhealthy_threshold_count=123,
   
)