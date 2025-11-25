#!/bin/bash
set -e

echo "=== Runtime Stockfish Installation ==="

# Check if stockfish is already installed
if [ ! -f "/usr/games/stockfish" ]; then
    echo "Stockfish not found, installing via apt..."
    
    # Update package list and install stockfish
    apt-get update -qq
    apt-get install -y -qq stockfish
    
    echo "✓ Stockfish installed"
else
    echo "✓ Stockfish already installed"
fi

echo "=== Stockfish Detection ==="

# Find stockfish
if [ -f "/usr/games/stockfish" ]; then
    STOCKFISH_BIN="/usr/games/stockfish"
    echo "✓ Found Stockfish at: /usr/games/stockfish"
elif [ -f "/usr/bin/stockfish" ]; then
    STOCKFISH_BIN="/usr/bin/stockfish"
    echo "✓ Found Stockfish at: /usr/bin/stockfish"
else
    echo "✗ ERROR: Stockfish still not found after installation!"
    echo "Checking locations:"
    ls -la /usr/games/ 2>/dev/null || echo "  /usr/games: not accessible"
    ls -la /usr/bin/stockfish 2>/dev/null || echo "  /usr/bin/stockfish: not found"
    exit 1
fi

echo "Stockfish binary: $STOCKFISH_BIN"

# Verify it's executable
if [ -x "$STOCKFISH_BIN" ]; then
    echo "✓ Stockfish is executable"
else
    echo "Making stockfish executable..."
    chmod +x "$STOCKFISH_BIN"
fi

# Test stockfish
echo "Testing Stockfish..."
$STOCKFISH_BIN --version || echo "✗ Warning: Could not get Stockfish version"

# Export for Python
export STOCKFISH_PATH="$STOCKFISH_BIN"
echo "✓ STOCKFISH_PATH exported: $STOCKFISH_PATH"

echo "=== Starting Python Server ==="
exec python main.py
