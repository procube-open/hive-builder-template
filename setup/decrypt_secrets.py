import os
import gnupg
import shutil
import subprocess

workdir = os.path.dirname(__file__) + "/.."
tmpdir = '/tmp'
if not os.getenv('HBSEC_PASSPHRASE'):
    print("HBSEC_PASSPHRASE is not set")
    exit(1)

# Decrypt secrets.gpg
os.makedirs(tmpdir + '/secrets', exist_ok=True)
os.makedirs(tmpdir + '/.gnupg', exist_ok=True)
gpg = gnupg.GPG(gnupghome=tmpdir + '/.gnupg')
gpg.encoding = 'utf-8'
gpg_file = workdir + '/secrets.gpg'
passphrase = os.getenv('HBSEC_PASSPHRASE')
gpg.decrypt_file(gpg_file, passphrase=passphrase, output=tmpdir + '/secrets.zip')
print("secrets.gpg decrypted to secrets.zip")

# Extract secrets.zip
subprocess.run(['unzip', 'secrets.zip'], stdout=subprocess.DEVNULL, cwd=tmpdir)
print("secrets.zip extracted to " + tmpdir + '/secrets')
for secret in os.listdir(tmpdir + '/secrets'):
    if os.path.isdir(tmpdir + '/secrets/' + secret):
        if os.path.exists(workdir + '/' + secret):
            answer = input(secret + " already exists. Overwrite? [y/N]: ")
            if answer.lower() != 'y':
                continue
            shutil.rmtree(workdir + '/' + secret)
        shutil.copytree(tmpdir + '/secrets/' + secret, workdir + '/' + secret)
    else:
        if os.path.exists(workdir + '/' + secret):
            answer = input(secret + " already exists. Overwrite? [y/N]: ")
            if answer.lower() != 'y':
                continue
            os.remove(workdir + '/' + secret)
        shutil.copy2(tmpdir + '/secrets/' + secret, workdir + '/' + secret)

# Remove temporary files
shutil.rmtree(tmpdir + '/secrets')
shutil.rmtree(tmpdir + '/.gnupg')
os.remove(tmpdir + '/secrets.zip')
print("/tmp/secrets removed")
