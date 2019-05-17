import sys
import getopt
import glob
import json
import os
import yaml
from IpSplitter import IPSplitter




def usage():
    '''
    THE fucniton that initalizes the entire class

    :return: THe HELP menu ?
    '''
    print('run_me.py -a <allocation> -c <cidr> \n ')
    print('-----------------------------------')
    print('-a , --alloc')
    print("\t  This is the allocation type to use e.g. 3AZSAD ")
    print('-c , --cidr')
    print("\t  This is the CIDR/Base range to use e.g. 192.168.0.0/23 ")


def config_loader():
    '''
    The configuration loader used to read all the yaml files and merge them into a single dictionary

    :return: Nested Dictionary containing all the yaml details
    '''
    configs = glob.glob(os.path.join(os.path.dirname(sys.argv[0]), 'configs/*.yaml'))

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
    '''
    Used to pass the required details to the IPsplitter class and then converts
    the response to vaild JSON for terraform's consumption

    :param vpc_range: The vpc range inputed to the program
    :param allocation: Type of subnetting method to use passed in from the CLI
    :return: List of ranges and there corisponding zones
    '''

    vpc_prefix = int(vpc_range.split('/')[1])
    allocation = allocation.upper()
    config = config_loader()[allocation]
    order = config['Order']
    subnetter = IPSplitter(vpc_range)

    data = {}
    for types in order:
        ip_count = config[vpc_prefix][types]['ips']
        cidr_prefix = config[vpc_prefix][types]['cidr']

        data[types] = ','.join(subnetter.get_subnet(cidr_prefix, ip_count))

    return data


def main(sysarg):
    '''
    The main function which initiates everything else, somehow this should be obvious

    :param sysarg: System args passed in
    :return: JSON response of all ranges and there zones
    '''

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
