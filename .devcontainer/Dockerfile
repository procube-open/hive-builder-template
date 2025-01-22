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
