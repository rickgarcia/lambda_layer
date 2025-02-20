#!/bin/bash
aws lambda publish-layer-version \
    --layer-name pytorch-transformers \
    --description "PyTorch and Transformers libraries for ML inference" \
    --zip-file fileb://pytorch-transformers-layer.zip \
    --compatible-runtimes python3.9 \
    --compatible-architectures x86_64
