#!/bin/bash

echo "Starting layer build process..."
echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la

echo "Creating Docker container to build packages..."
docker run --rm -v $(pwd):/var/task public.ecr.aws/sam/build-python3.9:latest \
    pip install -r requirements.txt -t python/ --verbose

echo "Contents of python directory after install:"
ls -la python/

echo "Creating layer zip file..."
zip -r pytorch-transformers-layer.zip python/

echo "Build complete. Layer size:"
ls -lh pytorch-transformers-layer.zip
