import json
import boto.ec2
from time import sleep
import argparse
__author__ = """{ 'name' : 'Amit Kumar Jaiswal', 'email' : 'amitkumarj441@gmail.com' }"""


parser = argparse.ArgumentParser(description="Launch AWS instance")
parser.add_argument("-f", "--file", help="Configuration input file", type=str, required=True)
args = parser.parse_args()
config_file = args.file


def create_security_group(conf_dict):
    """Create security group"""
    conn = boto.ec2.connect_to_region(conf_dict['region'])
    web = conn.create_security_group(conf_dict['security_group_name'], 'Only ssh and http access')
    web.authorize(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
    web.authorize(ip_protocol='tcp', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')
    print "Security group rules : ",
    print web.rules
    return web.id


def run_instance(conf_dict):
    conn = boto.ec2.connect_to_region(conf_dict['region'])

    reservation = conn.run_instances(
        conf_dict['image_id'],
        key_name=conf_dict['key_name'],
        instance_type=conf_dict['instance_type'],
        security_groups=[conf_dict['security_group_name']]
    )
    instance = reservation.instances[0]
    while instance.update() != "running":
        sleep(5)  # Run this in a green thread, ideally
        print "Waiting for instance ..."
    return instance.ip_address


if __name__ == "__main__":
    #### Open json file for reading configuration
    f_conf = open(config_file, "r")
    conf_dict = json.loads(f_conf.read())
    f_ip = open("ip_address.txt", "w")

    #create security group
    security_group_id = create_security_group(conf_dict)
    print "Created security group %s and id is %s" %(conf_dict['security_group_name'], security_group_id)

    #launch instance
    ip_address = run_instance(conf_dict)
    print "Public Ip address is : ", ip_address
    f_ip.writelines(ip_address)
    f_conf.close()
    f_ip.close()
