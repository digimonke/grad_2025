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

2.1) Install Graphviz system binary (required for crisp DAG rendering)

Graph drawing via pydot/graphviz needs the `dot` executable. Install it with Homebrew:

```bash
brew install graphviz
```

If you're on Apple Silicon and `dot` isn't found after install, ensure Homebrew is on your PATH:

```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify:

```bash
dot -V
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
- If you see `"dot" not found in path`, install Graphviz using Homebrew as shown above. The app will fall back to a NetworkX renderer if `dot` is missing, but Graphviz gives nicer, ranked layouts.

## Docker

Build the image (includes Graphviz for `dot`):

```bash
docker build -t thesis-app .
```

Run the container locally on port 8502:

```bash
docker run --rm -p 8502:8502 thesis-app
```

Notes:
- The container installs system Graphviz so `st.graphviz_chart` and pydot work without extra setup.
- The app binds to `0.0.0.0` and honors `$PORT` (defaults to 8502). For platforms like Cloud Run/Render, set `PORT` via environment.
