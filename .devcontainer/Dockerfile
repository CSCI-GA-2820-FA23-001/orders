# This image has selenium and chrome driver already installed
FROM rofrano/pipeline-selenium:latest

# Become a regular user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# USER $USERNAME

# Check if the group 'vscode' already exists
RUN getent group $USERNAME || groupadd --gid $USER_GID $USERNAME

# Check if the user 'vscode' already exists
RUN id -u $USERNAME &>/dev/null || useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash

# RUN useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
RUN usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME

# Add Python package requiremnets to the dev environment
WORKDIR /app
COPY requirements.txt .
RUN sudo pip install -U pip wheel && \
    sudo pip install -r requirements.txt

# Become a regular user for development
USER $USERNAME

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp; bash ./install-tools.sh