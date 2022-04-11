import aws_cdk.aws_ec2 as ec2


def get_pipeline_sg(self, name):
    return ec2.CfnSecurityGroupIngress(self, "PipelineSecurityGroupIngress",
                                       ip_protocol="tcp",
                                       cidr_ip="0.0.0.0/0",
                                       from_port=80,
                                       group_name=name,
                                       to_port=80
                                       )
