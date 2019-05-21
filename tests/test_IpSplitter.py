import pytest
from IpSplitter import IPSplitter
from netaddr import IPNetwork


def test_get_available_ranges():
    vpc_range = '192.168.0.0/23'
    splitter = IPSplitter(vpc_range)
    assert splitter.get_available_ranges() == [IPNetwork('192.168.0.0/23')]


def test_clean_response():
    vpc_range = '192.168.0.1/23'
    splitter = IPSplitter(vpc_range)
    assert '192.168.0.1/23' in splitter.clean_response(splitter.get_available_ranges())


def test_subnetter():
    vpc_range = '192.168.0.0/23'
    splitter = IPSplitter(vpc_range)
    subnets_with_avail = splitter.subnetter(splitter.get_available_ranges()[0], 27, 2) + splitter.get_available_ranges()
    assert subnets_with_avail == ['192.168.0.0/27', '192.168.0.32/27',
                                  IPNetwork('192.168.0.64/26'), IPNetwork('192.168.0.128/25'),
                                  IPNetwork('192.168.1.0/24')]


def test_get_subnet_return():
    vpc_range = '192.168.0.0/23'
    splitter = IPSplitter(vpc_range)
    ips = splitter.get_subnet(27, 6) + splitter.get_subnet(26, 3) + splitter.get_subnet(27, 3) + splitter.get_available_ranges()
    assert ips == ['192.168.0.0/27', '192.168.0.32/27', '192.168.0.64/27', '192.168.0.96/27',
                   '192.168.0.128/27', '192.168.0.160/27', '192.168.0.192/26', '192.168.1.0/26',
                   '192.168.1.64/26', '192.168.1.128/27', '192.168.1.160/27', '192.168.1.192/27',
                   IPNetwork('192.168.1.224/27')]