#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install LFS and pull large files
apt-get update && apt-get install -y git-lfs
git lfs install
git lfs pull

# Then do normal Django setup
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
