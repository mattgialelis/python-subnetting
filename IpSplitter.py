from netaddr import IPNetwork, cidr_merge, cidr_exclude


class IPSplitter(object):

    def __init__(self, base_range):
        '''
        THE fucniton that initalizes the entire class

        :param base_range: cidr prefix the starting range to work from
        :return: NOTHING
        '''
        self.avail_ranges = set((IPNetwork(base_range),))

    def get_subnet(self, prefix, ip_count=None):
        '''
        Function which produces the subnets that are returned, each subnet is produced one by one
        due to limiations in the netaddr class not being able to handle lists, this function works
        around that by running over the list items in get_available_ranges()

        :param prefix: cidr prefix
        :param ip_count: how many ips you need
        :return: a list of cidr ranges broken
        '''
        subnets = []
        while_count = 0

        while ip_count > len(subnets):
            try:
                inc_subnet = self.subnetter(self.get_available_ranges()[while_count], prefix, 1)
                subnets.append(inc_subnet[0])

            except ValueError:
                print('DEBUG: CANT SUBTRACT FROM AVAILABLE RANGE python'
                      ' var self.get_available_ranges()'
                      )
                while_count += 1

            except IndexError:
                print('DEBUG: WHILE_COUNT ERROR', while_count)
                print('REASON: Cant subtract requested ips from available ranges')
                print('Ranges:', self.get_available_ranges(),
                      '\n Requested Range Prefix:', prefix,
                      '\n Requested Amount:', ip_count,
                      )
                break

        if len(subnets) >= ip_count:
            return subnets

    def subnetter(self, ranges, prefix, count):
        '''
        Takes IP with Range and splits it from there, then removes it from the list of available.
        This funciton is used in thetry catch as if it cant be subtracted it rolls to the next one

        :param ranges: range available to subtract from
        :param prefix: cidr prefix required
        :param count: Will always be 1 refer to get_subnet()
        :return: a list of cidr ranges broken
        '''
        subnets = list(ranges.subnet(prefix, count=count))

        net = self.get_available_ranges()
        exclude = cidr_merge(subnets)
        for exclude_ip in exclude:
            if isinstance(net, list):
                net = self.loop_exculde(net, exclude_ip)
            else:
                net = cidr_exclude(net, exclude_ip)

        self.avail_ranges = set(net)
        return self.clean_response(subnets)

    def get_available_ranges(self):
        '''
        Returns the available list of ranges which ranges can be subtracted from

        :return: returns available list of ranges
        '''
        return sorted(self.avail_ranges, key=lambda x: x.prefixlen, reverse=True)

    def loop_exculde(self, net, exclude):
        '''
        Function to loop thru the available ranges and remove the ones that are
        no longer available.

        :param net: list of Ips from available ranges
        :param exclude: list or single ip to remove from availble ranges
        :return: List with used ranges subrtracted
        '''
        return_list = []
        for net_ip in net:
            cidr = cidr_exclude(net_ip, exclude)
            return_list.extend(cidr)

        return_list = list(set(return_list))
        return return_list

    def clean_response(self, subnets):
        '''
        Removes the IPnetwork type from all Ip's and converts them to strings

        :param subnets: list of ips requested
        :return: cleaned list of ips requested
        '''
        cleaned_list = []
        for subnet in subnets:
            cleaned_list.append(str(subnet))
        return cleaned_list
