import subprocess
import getpass
import os
import yaml
import inquirer
import time

user = getpass.getuser()
dir = os.path.dirname(__file__)


def name_validation(base_answers, current):
    if len(current) == 0:
        return False
    return True


base_questions = [
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
gcp_questions = [
    inquirer.Editor('gcp_credential',
                    message="Please paste GCP credential here"
                    )
]

base_answers = inquirer.prompt(base_questions)

subprocess.run(['hive', 'set', 'stage', base_answers['stage']])

# install dependencies
print('--- Install dependencies ---')
if not os.path.exists('.collections'):
    print('Ansible collection is not installed')
    print('Automatically start installation after 3 seconds.')
    time.sleep(3)
    subprocess.run(['hive', 'install-collection'])
    print('Ansible collection is installed')
if base_answers['provider'] == 'vagrant':
    try:
        subprocess.run(['vagrant', '--version'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print('Vagrant is not installed')
        print('Automatically start installation after 3 seconds.')
        time.sleep(3)
        subprocess.run([dir + '/install-vagrant.sh'], user=user)
        print('Vagrant is successfully installed')
    try:
        subprocess.run(['squid', '--version'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print('squid is not installed')
        print('Automatically start installation after 3 seconds.')
        time.sleep(3)
        subprocess.run([dir + '/install-squid.sh'])
        print('squid is successfully installed')
    subprocess.run(['hive', 'set', 'vagrant_proxy', 'http://192.168.121.1:3128'])
elif base_answers['provider'] == 'gcp' and not os.path.exists('gcp_credential.json'):
    gcp_answers = inquirer.prompt(gcp_questions)
    with open('gcp_credential.json', 'w') as file:
        file.write(gcp_answers['gcp_credential'])
print('--- Install dependencies is done ---')

# Update hive.yml
hive_yml = None
print('--- Update hive.yml ---')
with open('inventory/hive.yml') as file:
    hive_yml = yaml.load(file, Loader=yaml.FullLoader)

if hive_yml['name'] != base_answers['name']:
    print('hive name is changed:' + hive_yml['name'] + ' -> ' + base_answers['name'])
    hive_yml['name'] = base_answers['name']
if not hive_yml['stages'][base_answers['stage']]:
    print('stage is added:' + base_answers['stage'])
    hive_yml['stages'][base_answers['stage']] = {}
base_answers['number_of_hosts'] = int(base_answers['number_of_hosts'])
del base_answers['name']

for key in base_answers:
    if key == 'stage':
        continue
    elif key not in hive_yml['stages'][base_answers['stage']]:
        print(key + ' is added:' + str(base_answers[key]))
        hive_yml['stages'][base_answers['stage']][key] = base_answers[key]
    elif hive_yml['stages'][base_answers['stage']][key] != base_answers[key]:
        print(key + ' is changed:' + str(hive_yml['stages'][base_answers['stage']][key]) + ' -> ' + str(base_answers[key]))
        hive_yml['stages'][base_answers['stage']][key] = base_answers[key]

with open('inventory/hive.yml', 'w') as file:
    yaml.dump(hive_yml, file)
print('--- Update hive.yml is done ---')
