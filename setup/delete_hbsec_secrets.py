import os
from github import Github

workdir = os.path.dirname(__file__) + "/.."
gh = Github(os.environ['GITHUB_TOKEN'])
repo = gh.get_repo(os.environ['GITHUB_REPOSITORY'])

# get secrets
secrets = None
count = 0
while secrets == None or count != 0:
    secrets = repo.get_secrets("codespaces")
    count = secrets.totalCount
    if count == 0:
        print("No secrets found. Retrying...")
        continue
    for secret in secrets:
        if secret.name.startswith("HBSEC_"):
            repo.delete_secret(secret.name, "codespaces")
            print(secret.name + " deleted")
print("All secrets deleted")
