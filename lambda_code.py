import os
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Initialize model and tokenizer at global scope to take advantage of container reuse
model = None
tokenizer = None

def initialize_model():
    global model, tokenizer
    if model is None:
        # Load model and tokenizer
        model_name = "distilgpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
def lambda_handler(event, context):
    try:
        # Initialize model if not already loaded
        initialize_model()
        
        # Get input text from event
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
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

