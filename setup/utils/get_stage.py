import yaml

with open('/workspaces/hive-builder-template/.hive/persistents.yml') as file:
    persistents_obj = yaml.safe_load(file)
    print(persistents_obj["stage"]["global"])