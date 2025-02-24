FROM public.ecr.aws/lambda/python:3.9

# Install build dependencies
RUN yum update -y && \
    yum install -y \
    gcc \
    gcc-c++ \
    make \
    git \
    tar \
    gzip

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clone the model repository directly from Huggingface
RUN mkdir -p /opt/ml/model && \
    git clone https://huggingface.co/distilgpt2 /opt/ml/model/distilgpt2

ADD /pii_data opt/data/pii_data

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
