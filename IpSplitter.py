from netaddr import IPNetwork, cidr_merge, cidr_exclude


class IPSplitter(object):
    def __init__(self, base_range):
        self.avail_ranges = set((IPNetwork(base_range),))

    def get_subnet(self, prefix, ip_count=None):

        subnets = []
        i = 0
        while_count = 0

        while ip_count > len(subnets):
            try:
                inc_subnet = self.subnetter(self.get_available_ranges()[while_count], prefix, 1)
                subnets.append(inc_subnet[0])

            except ValueError as e:
                print('DEBUG: CANT SUBTRACT FROM AVAILABLE RANGE python var self.get_available_ranges()')
                while_count += 1

            except IndexError as e:
                print('DEBUG: WHILE_COUNT ERROR', while_count)
                break

        if len(subnets) >= ip_count:
            return subnets

    # Takes IP with Range and splits it from there, then removes it from the list of available
    def subnetter(self, ranges, prefix, count):
        subnets = list(ranges.subnet(prefix, count=count))

        net = self.get_available_ranges()
        exclude = cidr_merge(subnets)
        for exclude in exclude:
            if isinstance(net, list):
                net = self.loop_exculde(net, exclude)
            else:
                net = cidr_exclude(net, exclude)

        self.avail_ranges = set(net)
        return self.clean_response(subnets)

    def get_available_ranges(self):
        return sorted(self.avail_ranges, key=lambda x: x.prefixlen, reverse=True)

    def remove_avail_range(self, ip_network):
        self.avail_ranges.remove(ip_network)

    def loop_exculde(self, net, exclude):
        return_list = []
        for net in net:
            cidr = cidr_exclude(net, exclude)
            return_list.extend(cidr)

        return_list = list(set(return_list))
        return return_list

    def clean_response(self, subnets):
        cleaned_list = []
        for subnets in subnets:
            cleaned_list.append(str(subnets))
        return cleaned_list
