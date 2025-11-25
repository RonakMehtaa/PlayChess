#!/bin/bash
set -e

echo "=== Stockfish Detection Script ==="

# Check common Debian/Ubuntu locations first
if [ -f "/usr/games/stockfish" ]; then
    STOCKFISH_BIN="/usr/games/stockfish"
    echo "✓ Found Stockfish at: /usr/games/stockfish"
elif [ -f "/usr/bin/stockfish" ]; then
    STOCKFISH_BIN="/usr/bin/stockfish"
    echo "✓ Found Stockfish at: /usr/bin/stockfish"
else
    # Try which command
    STOCKFISH_BIN=$(which stockfish 2>/dev/null || echo "")
    
    if [ -n "$STOCKFISH_BIN" ]; then
        echo "✓ Found Stockfish in PATH: $STOCKFISH_BIN"
    else
        # Try Nix store as last resort
        STOCKFISH_BIN=$(find /nix/store -name stockfish -type f 2>/dev/null | head -n1 || echo "")
        if [ -n "$STOCKFISH_BIN" ]; then
            echo "✓ Found Stockfish in Nix store: $STOCKFISH_BIN"
        fi
    fi
fi

if [ -z "$STOCKFISH_BIN" ]; then
    echo "✗ ERROR: Stockfish not found!"
    echo ""
    echo "Diagnostics:"
    ls -la /usr/games/stockfish 2>/dev/null || echo "  /usr/games/stockfish: NOT FOUND"
    ls -la /usr/bin/stockfish 2>/dev/null || echo "  /usr/bin/stockfish: NOT FOUND"
    which stockfish 2>/dev/null || echo "  stockfish not in PATH"
    echo ""
    echo "Contents of /usr/games:"
    ls -la /usr/games/ 2>/dev/null || echo "  /usr/games directory not accessible"
    exit 1
else
    echo "Stockfish binary: $STOCKFISH_BIN"
    
    # Verify it's executable
    if [ -x "$STOCKFISH_BIN" ]; then
        echo "✓ Stockfish is executable"
    else
        echo "✗ Stockfish found but not executable, fixing permissions..."
        chmod +x "$STOCKFISH_BIN" || echo "✗ Could not make executable"
    fi
    
    # Test stockfish
    echo "Testing Stockfish..."
    $STOCKFISH_BIN --version || echo "✗ Warning: Could not get Stockfish version"
    
    # Export for Python
    export STOCKFISH_PATH="$STOCKFISH_BIN"
    echo "✓ STOCKFISH_PATH exported: $STOCKFISH_PATH"
fi

echo "=== Starting Python Server ==="
exec python main.py
