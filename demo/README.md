# Demo app (pip-based setup)

This project was refactored to use pip + virtual environments instead of conda.

## Quick start (macOS, zsh)

1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Run the Streamlit app

```bash
streamlit run Home.py --server.headless true --server.port 8502
```

Tip: You can also use the VS Code task "Run Streamlit app".

## Notes
- Tested with Python 3.12. If you use another version, adjust as needed.
- The old `environment.yml` (conda) is kept for reference. You can delete it once you're comfortable with the pip workflow.
- If you use a different virtual environment name (e.g., `venv`), update your VS Code Python interpreter accordingly.

## Common issues
- If you see runtime errors about missing packages, ensure your virtualenv is activated and reinstall with `pip install -r requirements.txt`.
- Some packages may compile native extensions on first install. Xcode Command Line Tools might be required on macOS: `xcode-select --install`.
