aws lambda publish-layer-version \
    --layer-name pytorch-transformers \
    --description "PyTorch and Transformers libraries for ML inference" \
    --content S3Bucket=sbx-lambda-layer-test,S3Key=pytorch-transformers-layer.zip \
    --compatible-runtimes python3.9 \
    --compatible-architectures x86_64
