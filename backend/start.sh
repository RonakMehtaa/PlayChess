#!/bin/bash
set -e

echo "Finding Stockfish..."
STOCKFISH_BIN=$(which stockfish 2>/dev/null || find /nix/store -name stockfish -type f 2>/dev/null | head -n1 || echo "")

if [ -z "$STOCKFISH_BIN" ]; then
    echo "ERROR: Stockfish not found!"
    echo "Checking common locations..."
    ls -la /usr/bin/stockfish 2>/dev/null || echo "/usr/bin/stockfish not found"
    ls -la /usr/games/stockfish 2>/dev/null || echo "/usr/games/stockfish not found"
    ls -la /nix/store/ | grep stockfish || echo "No stockfish in /nix/store"
else
    echo "Found Stockfish at: $STOCKFISH_BIN"
    export STOCKFISH_PATH="$STOCKFISH_BIN"
fi

echo "Starting Python server..."
python main.py
