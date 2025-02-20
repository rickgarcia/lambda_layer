#!/bin/bash

# Create a Docker container to build the packages
docker run --rm -v $(pwd):/var/task public.ecr.aws/sam/build-python3.9:latest \
    pip install -r requirements.txt -t python/

# Create the layer zip file
zip -r pytorch-transformers-layer.zip python/
