#!/bin/bash

# Check if sufficient arguments are provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Get the input filename
INPUT_FILE=$1

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found"
    exit 2
fi

# Define chunk size (10MB = 10485760 bytes)
CHUNK_SIZE=10485760

# Split the file
split -b $CHUNK_SIZE "$INPUT_FILE" "${INPUT_FILE}_chunk_"

echo "File '$INPUT_FILE' has been split into 10MB chunks with prefix '${INPUT_FILE}_chunk_'"
