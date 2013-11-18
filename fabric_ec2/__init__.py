from boto import ec2


class EC2TagManager:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, regions=None, common_tags=None):
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

    def get_instances(self, instance_attr='public_dns_name', **kwargs):
        """ Return instances that match the given tags.

            Keyword arguments:
            instance_attr -- attribute of instance(s) to return (default public_dns_name)

            Additional arguments are used to generate tag filter e.g. "get_instances(role='test')
        """
        if not instance_attr:
            raise ValueError('instance_attr cannot be None or empty' % instance_attr)

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
                    instance_value = getattr(instance, instance_attr)
                    if instance_value:
                        # Terminated/stopped instances will not have a public_dns_name
                        hosts.append(instance_value)
                    else:
                        raise ValueError('%s is not an attribute of instance' % instance_attr)
        return hosts
