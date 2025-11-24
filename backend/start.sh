#!/bin/bash
set -e

echo "Finding Stockfish..."

# Check common Debian/Ubuntu locations first
if [ -f "/usr/games/stockfish" ]; then
    STOCKFISH_BIN="/usr/games/stockfish"
elif [ -f "/usr/bin/stockfish" ]; then
    STOCKFISH_BIN="/usr/bin/stockfish"
else
    # Try which command
    STOCKFISH_BIN=$(which stockfish 2>/dev/null || echo "")
    
    # Try Nix store as last resort
    if [ -z "$STOCKFISH_BIN" ]; then
        STOCKFISH_BIN=$(find /nix/store -name stockfish -type f 2>/dev/null | head -n1 || echo "")
    fi
fi

if [ -z "$STOCKFISH_BIN" ]; then
    echo "ERROR: Stockfish not found!"
    echo "Checking common locations..."
    ls -la /usr/bin/stockfish 2>/dev/null || echo "/usr/bin/stockfish not found"
    ls -la /usr/games/stockfish 2>/dev/null || echo "/usr/games/stockfish not found"
    which stockfish || echo "stockfish not in PATH"
else
    echo "Found Stockfish at: $STOCKFISH_BIN"
    export STOCKFISH_PATH="$STOCKFISH_BIN"
    
    # Verify it's executable
    if [ -x "$STOCKFISH_BIN" ]; then
        echo "Stockfish is executable ✓"
        $STOCKFISH_BIN --version || echo "Warning: Could not get Stockfish version"
    else
        echo "ERROR: Stockfish found but not executable!"
        chmod +x "$STOCKFISH_BIN" || echo "Could not make executable"
    fi
fi

echo "Starting Python server..."
python main.py
