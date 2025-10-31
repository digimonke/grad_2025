# Streamlit app Dockerfile
# Base image with Python 3.12
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System packages:
# - graphviz: provides the `dot` binary required by graphviz/pydot and st.graphviz_chart
# - build-essential: compiler toolchain for any packages needing build
# - libgomp1: OpenMP runtime used by numpy/scikit-learn on some platforms
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    build-essential \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps first (better build cache)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application
COPY . /app

# Streamlit server defaults for containers
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PORT=8502

# Expose the default port (some platforms override via $PORT)
EXPOSE 8502

# Run the app; bind to 0.0.0.0 and honor $PORT if provided
CMD ["sh", "-c", "streamlit run Home.py --server.headless=true --server.address=0.0.0.0 --server.port=${PORT:-8502}"]
