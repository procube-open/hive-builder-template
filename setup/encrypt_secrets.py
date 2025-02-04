import os
import shutil
import gnupg
import string
import random
from github import Github

workdir = os.path.dirname(__file__) + "/.."
tmpdir = '/tmp'
gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])

os.makedirs(tmpdir + '/secrets', exist_ok=True)
secrets = [workdir + '/secrets.yml', workdir + '/gcp_credential.json', workdir + '/.env']
for secret in secrets:
    if os.path.exists(secret):
        shutil.copy2(secret, tmpdir + '/secrets/' + os.path.basename(secret))

stages = ["private", "staging", "production"]
skip_files = ["Vagrantfile", "vagrant.log", "vagrant_vars.yml", "growfs.sh", ".vagrant"]
os.makedirs(tmpdir + '/secrets/.hive', exist_ok=True)
if os.path.exists(workdir + '/.hive/persistents.yml'):
    shutil.copy2(workdir + '/.hive/persistents.yml', tmpdir + '/secrets/.hive/persistents.yml')
for stage in stages:
    if os.path.exists(workdir + '/.hive/' + stage):
        os.makedirs(tmpdir + '/secrets/.hive/' + stage, exist_ok=True)
        for file in os.listdir(workdir + '/.hive/' + stage):
            if file in skip_files:
                continue
            if os.path.isdir(workdir + '/.hive/' + stage + '/' + file):
                shutil.copytree(workdir + '/.hive/' + stage + '/' + file, tmpdir + '/secrets/.hive/' + stage + '/' + file)
            else:
                shutil.copy2(workdir + '/.hive/' + stage + '/' + file, tmpdir + '/secrets/.hive/' + stage + '/' + file)

shutil.make_archive(tmpdir + '/secrets', 'zip', tmpdir + '/secrets')
print("secrets.zip created")

length = 32
characters = string.ascii_letters + string.digits + string.punctuation
passphrase = ''.join(random.choice(characters) for i in range(length))
print("Generated passphrase: " + passphrase)
os.makedirs(tmpdir + '/.gnupg', exist_ok=True)
gpg = gnupg.GPG(gnupghome=tmpdir + '/.gnupg')
gpg.encoding = 'utf-8'
gpg_file = workdir + '/secrets.gpg'
encrypted_secrets = gpg.encrypt_file(tmpdir + '/secrets.zip', recipients=None, symmetric=True, output=gpg_file, passphrase=passphrase)
print("secrets.zip encrypted to secrets.gpg with passphrase")

repo.create_secret("HBSEC_PASSPHRASE", passphrase, "codespaces")
print("HBSEC_PASSPHRASE exported")

shutil.rmtree(tmpdir + '/secrets')
shutil.rmtree(tmpdir + '/.gnupg')
os.remove(tmpdir + '/secrets.zip')
