#!/bin/bash

ssh -F /workspaces/hive-builder-template/.hive/private/ssh_config -t p-hive0.test "sudo bash -c 'echo -e \"[global]\ntrusted-host = pypi.org files.pythonhosted.org pypi.python.org\" > /etc/pip.conf'"
ssh -F /workspaces/hive-builder-template/.hive/private/ssh_config -t p-hive1.test "sudo bash -c 'echo -e \"[global]\ntrusted-host = pypi.org files.pythonhosted.org pypi.python.org\" > /etc/pip.conf'"
ssh -F /workspaces/hive-builder-template/.hive/private/ssh_config -t p-hive2.test "sudo bash -c 'echo -e \"[global]\ntrusted-host = pypi.org files.pythonhosted.org pypi.python.org\" > /etc/pip.conf'"