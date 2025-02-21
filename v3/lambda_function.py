import json
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Set model path
MODEL_PATH = "/opt/ml/model/distilgpt2"

# Initialize model and tokenizer at global scope
model = None
tokenizer = None

def initialize_model():
    global model, tokenizer
    if model is None:
        print(f"Loading model from {MODEL_PATH}")
        # Load model and tokenizer from local path
        tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
        model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
        print("Model loaded successfully")
        
def lambda_handler(event, context):
    try:
        # Validate input before initializing the model
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No body found in event'})
            }
            
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        input_text = body.get('text', '')
        
        if not input_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No text provided in request body'})
            }
            
        # Only initialize model after validating the request
        initialize_model()
        
        # Tokenize input
        inputs = tokenizer(input_text, return_tensors="pt")
        
        # Generate text
        with torch.no_grad():
            outputs = model.generate(
                inputs['input_ids'],
                max_length=100,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode and return generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'input_text': input_text,
                'generated_text': generated_text
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'traceback': traceback.format_exc()
            })
        }
