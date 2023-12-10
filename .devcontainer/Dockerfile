# This image has selenium and chrome driver already installed
FROM rofrano/pipeline-selenium:latest

# Become a regular user for development
ARG USERNAME=vscode
USER $USERNAME

# Create the user with passwordless sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
    
# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp; bash ./install-tools.sh

# Add Python package requiremnets to the dev environment
WORKDIR /app
COPY requirements.txt .
RUN sudo pip install -U pip wheel && \
    sudo pip install -r requirements.txt