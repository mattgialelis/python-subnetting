import sys, getopt
import yaml
import glob
from IpSplitter import IPSplitter
import json

def usage():
    print('run_me.py -a <allocation> -c <cidr> \n ')
    print('-----------------------------------')
    print('-a , --alloc')
    print("\t  This is the allocation type to use e.g. 3AZSAD ")
    print('-c , --cidr')
    print("\t  This is the CIDR/Base range to use e.g. 192.168.0.0/23 ")


def config_loader():
    configs = glob.glob('configs/*.yaml')
    merged_config = {}

    for conf_file in configs:
        with open(conf_file, 'r') as stream:
            try:
                yaml_config = yaml.safe_load(stream)
                merged_config.update(yaml_config)

            except yaml.YAMLError as exc:
                print(exc)

    return merged_config


def subnet_producer(vpc_range, allocation):

    vpc_prefix = int(vpc_range.split('/')[1])
    allocation = allocation.upper()
    config = config_loader()[allocation]
    order = config['Order']
    # print('VPC Prefix:', vpc_prefix, 'Allocation:', allocation)
    subnetter = IPSplitter(vpc_range)

    data = {}
    for types in order:
        ip_count = config[vpc_prefix][types]['ips']
        cidr_prefix = config[vpc_prefix][types]['cidr']

        # print('--------------', type.upper(), '------ Range Count: ', ip_count,'------ Prefix: ', cidr_prefix,'--------')
        data[types] = subnetter.get_subnet(cidr_prefix, ip_count)
    return  data

def main(sysarg):
    try:
        opts, args = getopt.getopt(sysarg, 'a:c:h', ['alloc=', 'cidr=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-a', '--alloc'):
            allocation = arg
        elif opt in ('-c', '--cidr'):
            cidr = arg
        else:
            usage()
            sys.exit(2)

    print(json.dumps(subnet_producer(cidr, allocation)))


if __name__ == "__main__":
   main(sys.argv[1:])
