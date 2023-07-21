#!/bin/bash

# Check if the correct number of arguments are provided
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "Usage: $0 <depth> <fen> [<moves>]"
  exit 1
fi

# Get the arguments
depth=$1
fen=$2
moves=$3

# Run your chess engine's perft function and capture the output
output=$(python perftree.py "$depth" "$fen" "$moves")

# Print the move counts
echo "$output"
