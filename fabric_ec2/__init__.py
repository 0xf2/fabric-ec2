from boto import ec2


class EC2TagManager:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, regions=None, common_tags=None) :
        """ This class helps find instances with a particular set of tags.
        
            If access key/secret are not given, they must be available as environment
            variables so boto can access them.
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.common_tags = common_tags if common_tags else {}
        # todo get full region list
        self.regions = regions if regions else ['us-east-1']
        # Open connections to ec2 regions
        self.conn = {}
        for region in self.regions:
            self.conn[region] = ec2.connect_to_region(region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key)

    def _build_tag_filter(self, tags):
        """ Convert a dict in to a tag filter.
        
            Given a dict {'key': 'val'}, return {'tag:key': 'val'}.
        """
        tag_filter = {}
        for k, v in tags.iteritems():
            tag_filter['tag:%s' % k] = v
        return tag_filter
            

    def get_instances(self, **kwargs):
        """ Return instances that match the given tags. Tags are specified
            as kwargs, e.g. "get_instances(role='test')
        """
        tags = self.common_tags
        for k, v in kwargs.copy().iteritems():
            tags[k] = v
            kwargs.pop(k)

        tag_filter = self._build_tag_filter(tags)

        hosts = []
        for region in self.regions:
            reservations = self.conn[region].get_all_instances(None, tag_filter)
            for res in reservations:
                for instance in res.instances:
                    if instance.public_dns_name != '':
                        # Terminated/stopped instances will not have a public_dns_name
                        hosts.append(instance.public_dns_name)
        return hosts
