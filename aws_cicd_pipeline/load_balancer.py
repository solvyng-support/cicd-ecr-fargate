from aws_cdk.core import Arn
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_ec2 as ec2
import os


def get_app_lb(self, name: str,  security_group: ec2.SecurityGroup):
    return elbv2.CfnLoadBalancer(self, "CfnLoadBalancer",
                                 ip_address_type="ipv4",
                                 name=name,
                                 security_groups=[security_group.security_group_id],
                                 type="application"
                                 )


def get_lb_listener(self, alb: elbv2.ILoadBalancerV2):
    return elbv2.CfnListener(self, "CfnListener",
                             load_balancer_arn=alb.load_balancer_arn,
                             port=80,
                             protocol="tcp",
                             )


def get_pipeline_tg(self, name):
    return elbv2.CfnTargetGroup(self, "CfnTargetGroup",
                                ip_address_type="ipv4",
                                name=name,
                                port=80,
                                protocol="tcp",
                                protocol_version="HTTP1",
                                target_type="ip",
                                )


def get_lb_listener_rule(self, pipeline_tg: elbv2.ITargetGroup, alb_listener: elbv2.IApplicationListener):
    return elbv2.CfnListenerRule(self, "CfnListenerRule",
                                 actions=[elbv2.CfnListenerRule.ActionProperty(
                                     type="forward",
                                     forward_config=elbv2.CfnListenerRule.ForwardConfigProperty(
                                         target_groups=[elbv2.CfnListenerRule.TargetGroupTupleProperty(
                                             target_group_arn=pipeline_tg.target_group_arn,
                                             weight=1
                                         )],
                                     ),
                                 )],
                                 listener_arn=alb_listener.listener_arn,
                                 priority=1
                                 )
