#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run any additional build steps here
# For example, if you need to run tests or lint your code, do it here
# echo "Running tests..."
# pytest

# Print a success message
echo "Build complete!"
