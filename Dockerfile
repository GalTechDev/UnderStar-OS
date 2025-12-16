
FROM python:3.9-slim

WORKDIR /app

# Install git for gitpython
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy library and setup files
COPY understar/ /app/understar/
COPY setup.py /app/
COPY README.md /app/
COPY MANIFEST.in /app/

# Install the library
RUN pip install .

# Copy the entry point script
COPY exemple.py /app/main.py

# Create volume mount points
VOLUME ["/app/data", "/app/plugins"]

# Entry point
CMD ["python", "main.py"]