import yaml
import json


class TransformFile:
    def __init__(self):
        pass

    def read_file(self):
        file = 'serverless.yml'

        with open(file, 'r') as reader:
            full_file: dict = yaml.load(reader.read(), Loader=yaml.BaseLoader)

            resources: dict = full_file.get('Resources')

            if resources is None:
                resources: dict = full_file.get('resources').get('Resources')

            items_full: list = [resources.get(item).get('Type') for item in resources]
            items_uniq: list = []

            for item in dict.fromkeys(items_full):

                item_origin: str = item.split('::')[1].lower()
                item_final: str = item.split('::')[2]
                resource_info = {item_origin: item_final}

                items_uniq.append(resource_info)

            aws: object = AmazonFile()
            basic_policy: dict = aws.base_policy()

            for action in items_uniq:
                statement: dict = aws.create_policy(action)

                basic_policy['Statement'].append(statement)

            with open('policy.json', 'w+') as policy_file:
                policy = json.dumps(basic_policy, indent=4)
                print(policy)
                policy_file.write(policy)


class AmazonFile:
    def __init__(self):
        pass

    def create_policy(self, action: dict):
        statement: dict = {}
        resource = list(action.keys())[0]
        dest: str = ''
        #TODO: Make this better
        if action[resource] == 'VPC':
            dest: str = 'CreateVpc'
        if action[resource] == 'InternetGateway':
            dest: str = 'CreateInternetGateway'
        if action[resource] == 'Subnet':
            dest: str = 'CreateSubnet'
        if action[resource] == 'RouteTable':
            dest: str = 'CreateRouteTable'
        if action[resource] == 'Route':
            dest: str = 'CreateRoute'
        if action[resource] == 'VPCEndpoint':
            dest: str = 'CreateVpcEndpoint'
        if action[resource] == 'Bucket':
            dest: str = 'CreateBucket'
        if action[resource] == 'BucketPolicy':
            dest: str = 'PutBucketPolicy'
        if action[resource] == 'Distribution':
            dest: str = 'CreateDistribution'
        else:
            pass

        statement['Effect'] = 'Allow'
        statement['Resource'] = f'*'
        statement['Action'] = f'{resource}:{dest}'
        return statement

    def base_policy(self):
        policy: dict = {}
        policy['Version'] = "2012-10-17"
        policy['Statement'] = []
        return policy


if __name__ == '__main__':
    tr: object = TransformFile()
    tr.read_file()