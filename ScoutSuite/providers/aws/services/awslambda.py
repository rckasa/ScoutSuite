# -*- coding: utf-8 -*-
from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.aws.configs.regions_config import RegionsConfig
from ScoutSuite.providers.aws.aws_facade import AWSFacade
from opinel.utils.aws import build_region_list


class LambdaServiceConfig(RegionsConfig):
    def __init__(self):
        super(LambdaServiceConfig, self).__init__('lambda')

    async def fetch_all(self, regions=None, partition_name='aws'):
        await super(LambdaServiceConfig, self).fetch_all(
            chosen_regions=regions,
            partition_name=partition_name
        )

        for region in self['regions']:
            self['regions'][region] = await RegionalLambdas().fetch_all(region=region)
            await functions.fetch_all(region=region)
            self['regions'][region] = functions


class RegionalLambdas(Resources):
    async def fetch_all(self, region):
        # TODO: Should be injected
        facade = AWSFacade()

        functions = {}
        for raw_function in facade.get_lambda_functions(region):
            name, function = self.parse_function(raw_function)
            functions[name] = function

        self['functions_count'] = len(functions)
        self['functions'] = functions
        return self

    @staticmethod
    def parse_function(function):
        function['name'] = function.pop('FunctionName')
        return (function['name'], function)
