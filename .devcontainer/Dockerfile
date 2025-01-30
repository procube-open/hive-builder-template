FROM mcr.microsoft.com/vscode/devcontainers/python:3

RUN apt-get update
RUN apt-get install -y vim tcpdump network-manager

RUN apt-get install -y systemd
RUN ln -sf /lib/systemd/systemd /sbin/init

# Make virtual environment
RUN python3 -m venv /opt/hive
RUN chown -hR vscode:vscode /opt/hive

# Install Python packages
RUN /opt/hive/bin/pip install --upgrade pip
RUN /opt/hive/bin/pip install ansible-core ansible-dev-tools setuptools hive-builder inquirer google-cloud-compute

# Setup bash completion
RUN echo "source \$(/opt/hive/bin/hive get-install-dir)/hive-completion.sh" >> /home/vscode/.bashrc

ENTRYPOINT ["/sbin/init"]