
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Upgrading pip into venv..."
.venv/bin/python -m pip install --upgrade pip

echo "Updating Python dependencies into venv..."
.venv/bin/python -m pip install -r requirements.txt

echo "Setup complete."