#!/bin/bash
set -euo pipefail

echo "Upgrading pip..."
pip install --upgrade pip || {
    echo "Failed to upgrade pip"
    exit 1
}

echo "🔧 Installing NVM..."
export NVM_DIR="$HOME/.nvm"
mkdir -p "$NVM_DIR"

# Download and install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash || {
    echo "Failed to download NVM installer"
    exit 1
}

# Add NVM to bashrc for future sessions
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc

# Load NVM for current session
if [ -s "$NVM_DIR/nvm.sh" ]; then
    \. "$NVM_DIR/nvm.sh"
    echo "NVM loaded successfully"
else
    echo "NVM script not found at $NVM_DIR/nvm.sh"
    exit 1
fi

# Verify NVM is available
if ! command -v nvm &> /dev/null; then
    echo "NVM command not found after sourcing. Trying alternative approach..."
    # Try to source it with bash explicitly
    bash -c "source $NVM_DIR/nvm.sh && nvm --version" || {
        echo "Failed to verify NVM installation"
        exit 1
    }
fi

echo "📦 Installing Node.js LTS..."
# Run nvm commands in a bash subshell to ensure proper environment
bash -c "source $NVM_DIR/nvm.sh && nvm install --lts" || {
    echo "Failed to install Node.js"
    exit 1
}

# Run nvm use in a bash subshell
bash -c "source $NVM_DIR/nvm.sh && nvm use --lts" || {
    echo "Failed to use Node.js LTS"
    exit 1
}

echo "🧰 Installing latest npm..."
# Run npm in a bash subshell to ensure node is available
bash -c "source $NVM_DIR/nvm.sh && nvm use --lts && npm install -g npm@latest" || {
    echo "Failed to update npm"
    exit 1
}

echo "✅ NVM, Node.js, and npm installed successfully."

if [ -f requirements.txt ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt || {
        echo "Failed to install requirements"
        exit 1
    }
else
    echo "No requirements.txt found, skipping package installation"
fi

echo "Setting up terminal prompt..."
cat << 'EOF' >> ~/.bashrc
# Function to get git branch
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# Color definitions
BLUE='\[\033[34m\]'
GREEN='\[\033[32m\]'
YELLOW='\[\033[33m\]'
RESET='\[\033[00m\]'

# Set prompt with current directory and git branch
export PS1="${BLUE}\W${RESET}${YELLOW}\$(parse_git_branch)${RESET}${GREEN} $ ${RESET}"
EOF

export ENABLE_BACKGROUND_TASKS=1

echo "Setup completed successfully!" 