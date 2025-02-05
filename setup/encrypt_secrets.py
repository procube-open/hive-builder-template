import os
import shutil
import subprocess
import gnupg
import string
import random
from github import Github

workdir = os.path.dirname(__file__) + "/.."
tmpdir = '/tmp'
gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])
workdir_secrets = ['secrets.yml', 'gcp_credential.json', '.env']
stages = ["private", "staging", "production"]
skip_files = ["Vagrantfile", "vagrant.log", "vagrant_vars.yml", "growfs.sh", ".vagrant"]

# Create secrets.zip
if os.path.exists(tmpdir + '/secrets'):
    shutil.rmtree(tmpdir + '/secrets')
if os.path.exists(tmpdir + '/secrets.zip'):
    os.remove(tmpdir + '/secrets.zip')
os.makedirs(tmpdir + '/secrets', exist_ok=True)
for secret in workdir_secrets:
    if os.path.exists(workdir + '/' + secret):
        shutil.copy2(workdir + '/' + secret, tmpdir + '/secrets/' + secret)

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

subprocess.run(['zip', '-r', 'secrets.zip', 'secrets'], stdout=subprocess.DEVNULL, cwd=tmpdir)
print("secrets.zip created")

# Generate passphrase
length = 32
characters = string.ascii_letters + string.digits + string.punctuation
passphrase = ''.join(random.choice(characters) for i in range(length))
print("passphrase generated: " + passphrase)

# Encrypt secrets.zip
os.makedirs(tmpdir + '/.gnupg', exist_ok=True)
gpg = gnupg.GPG(gnupghome=tmpdir + '/.gnupg')
gpg.encoding = 'utf-8'
gpg_file = workdir + '/secrets.gpg'
encrypted_secrets = gpg.encrypt_file(tmpdir + '/secrets.zip', recipients=None, symmetric=True, output=gpg_file, passphrase=passphrase)
print("secrets.zip encrypted to secrets.gpg with passphrase")

# Export HBSEC_PASSPHRASE
repo.create_secret("HBSEC_PASSPHRASE", passphrase, "codespaces")
print("passphrase exported to HBSEC_PASSPHRASE")

# Remove temporary files
shutil.rmtree(tmpdir + '/secrets')
shutil.rmtree(tmpdir + '/.gnupg')
os.remove(tmpdir + '/secrets.zip')
