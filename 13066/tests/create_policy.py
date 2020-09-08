from ruamel.yaml import YAML
import ruamel.yaml
from ast import literal_eval

file_name = 'custom_policy.yaml'
yaml2 = YAML(typ='safe')
config = yaml2.load(open(file_name))

# yaml = YAML()
# config = yaml.load(open(file_name))
print((config['metadata']['name']))
policies = literal_eval(config['data']['policies'])
policies.append({'abc': 'def'})
config['data']['policies'] = str(policies)



# print(policies)
# policies.append({"resource": {}, "match": []})

with open('output.yaml', 'w') as fp:
  ruamel.yaml.dump(config, fp, Dumper=ruamel.yaml.RoundTripDumper)
