import subprocess
import getpass
import os
import yaml
import inquirer
import time

user = getpass.getuser()

def name_validation(answers, current):
    if len(current) == 0:
        return False
    return True

questions = [
    inquirer.Text('name',
                  message="What's hive name?",
                  validate=name_validation,
                  ),
    inquirer.List('stage',
                  message="What stage do you want to use?",
                  choices=['private', 'staging', 'production'],
                  ),
    inquirer.List('provider',
                  message="What provider do you want to use?",
                  choices=['vagrant', 'gcp', 'aws',
                           'azure', 'kickstart', 'prepared'],
                  ),
    inquirer.Text('cidr',
                  message="What's the CIDR?",
                  default='192.168.0.0/16'
                  ),
    inquirer.Confirm('separate_repository',
                     message="Do you want to use a separate repository?",
                     default=False,
                     ),
    inquirer.Text('number_of_hosts',
                  message="How many hosts do you want to create?",
                  validate=lambda _, x: x.isdigit(),
                  default='3',
                  )
]
answers = inquirer.prompt(questions)

subprocess.run(['hive', 'set', 'stage', answers['stage']])

# install dependencies
print('--- Install dependencies ---')
if not os.path.exists('.collections'):
    print('Ansible collection is not installed')
    print('Automatically start installation after 3 seconds.')
    time.sleep(3)
    subprocess.run(['hive', 'install-collection'])
    print('Ansible collection is installed')
if answers['provider'] == 'vagrant':
    try:
        subprocess.run(['vagrant', '--version'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print('Vagrant is not installed')
        print('Automatically start installation after 3 seconds.')
        time.sleep(3)
        subprocess.run(['install-vagrant.sh'], user=user)
        subprocess.run(['install-squid.sh'])
        print('Vagrant is installed')
elif answers['provider'] == 'gcp' and not os.path.exists('gcp_credential.json'):
    gcp_answers = inquirer.prompt([
        inquirer.Editor('gcp_credential',
                        message="Please paste GCP credential here",
                        )
    ])
    with open('gcp_credential.json', 'w') as file:
        file.write(gcp_answers['gcp_credential'])
print('--- Install dependencies is done ---')

# Update hive.yml
hive_yml = None
print('--- Update hive.yml ---')
with open('inventory/hive.yml') as file:
    hive_yml = yaml.load(file, Loader=yaml.FullLoader)
if hive_yml['name'] != answers['name']:
    print('hive name is changed:' +
          hive_yml['name'] + ' -> ' + answers['name'])
    hive_yml['name'] = answers['name']
if hive_yml['stages'][answers['stage']]['provider'] != answers['provider']:
    print('provider is changed:' +
          hive_yml['stages'][answers['stage']]['provider'] + ' -> ' + answers['provider'])
    hive_yml['stages'][answers['stage']]['provider'] = answers['provider']
if hive_yml['stages'][answers['stage']]['cidr'] != answers['cidr']:
    print('cidr is changed:' +
          hive_yml['stages'][answers['stage']]['cidr'] + ' -> ' + answers['cidr'])
    hive_yml['stages'][answers['stage']]['cidr'] = answers['cidr']
if hive_yml['stages'][answers['stage']]['separate_repository'] != answers['separate_repository']:
    print('separate_repository is changed:' +
          str(hive_yml['stages'][answers['stage']]['separate_repository']) + ' -> ' + str(answers['separate_repository']))
    hive_yml['stages'][answers['stage']
                       ]['separate_repository'] = answers['separate_repository']
if hive_yml['stages'][answers['stage']]['number_of_hosts'] != int(answers['number_of_hosts']):
    print('number_of_hosts is changed:' +
          str(hive_yml['stages'][answers['stage']]['number_of_hosts']) + ' -> ' + answers['number_of_hosts'])
    hive_yml['stages'][answers['stage']]['number_of_hosts'] = int(
        answers['number_of_hosts'])
with open('inventory/hive.yml', 'w') as file:
    yaml.dump(hive_yml, file)
print('--- Update hive.yml is done ---')
