import aws_cdk.aws_ec2 as ec2


def get_pipelineSG(self, name):
    return ec2.CfnSecurityGroupIngress(self, "MyCfnSecurityGroupIngress",
    ip_protocol="tcp",

    # the properties below are optional
    cidr_ip="0.0.0.0/0",
    #cidr_ipv6="cidrIpv6",
    #description="description",
    from_port= 80,
    #group_id="groupId",
    group_name= name ,
    #source_prefix_list_id="sourcePrefixListId",
    #source_security_group_id="sourceSecurityGroupId",
    #source_security_group_name="sourceSecurityGroupName",
    #source_security_group_owner_id="sourceSecurityGroupOwnerId",
    to_port= 80
)