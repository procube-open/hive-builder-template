FROM mcr.microsoft.com/vscode/devcontainers/python:3

USER root

# Install additional packages
RUN apt-get update

# Make virtual environment
RUN python3 -m venv /opt/hive
ENV PATH="/opt/hive/bin:$PATH"

# Install Python packages
RUN pip install --upgrade pip
RUN pip install ansible-core setuptools hive-builder

# Setup bash completion
RUN echo "source \$(/opt/hive/bin/hive get-install-dir)/hive-completion.sh" >> /home/vscode/.bashrc
RUN echo "alias pip='/opt/hive/bin/pip'" >> /home/vscode/.bashrc
ENV HIVE_VIRTUAL_ENV_INIT=1

# install collection
RUN hive install-collection

CMD ["/bin/bash"]
