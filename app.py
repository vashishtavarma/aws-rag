import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Retrieve environment variables
kb_id = os.environ.get("KNOWLEDGE_BASE_ID")
guardrail_id = os.environ.get("GUARDRAIL_ID")
guardrail_version = os.environ.get("GUARDRAIL_VERSION")
region = os.environ.get("REGION_NAME")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Create a boto3 session with credentials and initialize the Bedrock client with region
boto3_session = boto3.session.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
)
bedrock_agent_runtime_client = boto3_session.client('bedrock-agent-runtime')

model_arn = os.environ.get("MODEL_ARN")

def retrieve_and_generate_with_guardrails(input_text, kbId):
    response = bedrock_agent_runtime_client.retrieve_and_generate(
        input={
            'text': input_text
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kbId,
                'modelArn': model_arn,
                'generationConfiguration': {
                    'guardrailConfiguration': {
                        'guardrailId': guardrail_id,
                        'guardrailVersion': guardrail_version
                    },
                    'inferenceConfig': {
                        'textInferenceConfig': {
                            'maxTokens': 2048,
                            'temperature': 0.7,
                            'topP': 0.9,
                            'stopSequences': []
                        }
                    },
                    'promptTemplate': {
                        'textPromptTemplate': '''You are a helpful AI assistant. Use the following context to answer the user's question accurately and concisely.
                                                Context: $search_results$
                                                Question: $query$
                                                Answer:'''
                    }
                },
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': 5
                    }
                }
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )

    return response


def lambda_handler(event):
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
    result = lambda_handler(test_event)
    print(result["body"]["answer"]["output"]["text"])
