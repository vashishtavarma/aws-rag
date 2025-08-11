import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables
kb_id = os.environ.get("KNOWLEDGE_BASE_ID")
guardrail_id = os.environ.get("GUARDRAIL_ID")
guardrail_version = os.environ.get("GUARDRAIL_VERSION")
region = os.environ.get("REGION_NAME")

# Create a boto3 session and initialize the Bedrock client with region
boto3_session = boto3.session.Session()
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime', region_name=region)

llama_model_arn = os.environ.get("LLAMA_MODEL_ARN")

def retrieve_and_generate_with_guardrails(input_text, kbId):
    response = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': input_text
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kbId,
                'modelArn': llama_model_arn,
                'generationConfiguration': {
                    'guardrailConfiguration': {
                        'guardrailId': guardrail_id,
                        'guardrailVersion': guardrail_version
                    }
                },
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': 1
                    }
                }
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )

    return response


def lambda_handler(event, context):
    if 'question' not in event:
        return {
            'statusCode': 400,
            'body': 'No question provided.'
        }

    query = event['question']
    response = retrieve_and_generate_with_guardrails(query, kb_id)

    return {
        'statusCode': 200,
        'body': {
            "question": query.strip(),
            "answer": response
        }
    }

if __name__ == "__main__":
    test_event = {
        'question': 'Question'
    }
    result = lambda_handler(test_event, None)
    print(result["body"]["answer"]["output"]["text"])
