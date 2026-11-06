
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Upgrading pip into venv..."
.venv/bin/python -m pip install --upgrade pip

echo "Installing Python dependencies into venv..."
.venv/bin/python -m pip install -r requirements.txt

echo "Setup complete."