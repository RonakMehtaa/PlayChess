# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install stockfish and required system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends stockfish && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify stockfish is installed and show its location
RUN ls -la /usr/games/stockfish && /usr/games/stockfish --version

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variable for Stockfish path
ENV STOCKFISH_PATH=/usr/games/stockfish

# Expose port (Railway will override this)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
