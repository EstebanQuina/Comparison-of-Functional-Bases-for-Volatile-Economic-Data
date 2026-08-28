#!/bin/bash
# ============================================================
# Thesis Project: Functional Bases for Volatile Economic Series
# Environment Setup Script
# ============================================================
# Run this script from your project root directory:
#   cd /path/to/your/project
#   bash setup_environment.sh

echo "========================================"
echo " Setting up thesis project environment"
echo "========================================"

# Step 1: Create virtual environment
echo ""
echo "[1/3] Creating virtual environment 'fda_env'..."
python3 -m venv fda_env

# Step 2: Activate and install packages
echo ""
echo "[2/3] Installing required packages..."
source fda_env/bin/activate

pip install --upgrade pip

pip install \
    pandas \
    numpy \
    scipy \
    matplotlib \
    seaborn \
    scikit-learn \
    scikit-fda \
    PyWavelets \
    statsmodels \
    jupyter \
    notebook \
    ipykernel

# Step 3: Register kernel for Jupyter
echo ""
echo "[3/3] Registering Jupyter kernel..."
python -m ipykernel install --user --name=fda_env --display-name "Thesis FDA (Python 3)"

echo ""
echo "========================================"
echo " Setup complete!"
echo "========================================"
echo ""
echo "To activate your environment, run:"
echo "   source fda_env/bin/activate"
echo ""
echo "To launch Jupyter Notebook, run:"
echo "   jupyter notebook"
echo ""
echo "To deactivate the environment, run:"
echo "   deactivate"
