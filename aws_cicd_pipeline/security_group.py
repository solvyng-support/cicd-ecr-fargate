import aws_cdk.aws_ec2 as ec2


def get_securitygroup(self, name) -> ec2.CfnSecurityGroup:
    return ec2.CfnSecurityGroup(self, "CfnSecurityGroup",
                                group_description="groupDescription", 
                                security_group_ingress=get_ingress(self, name) )

def get_ingress(self, name) -> ec2.CfnSecurityGroupIngress:
    return ec2.CfnSecurityGroupIngress(self, "CfnSecurityGroupIngress",
                                       ip_protocol="tcp",
                                       cidr_ip="0.0.0.0/0",
                                       from_port=80,
                                       group_name=name,
                                       to_port=80
                                       )

