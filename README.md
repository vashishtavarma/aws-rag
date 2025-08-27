# AWS RAG Application

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/bedrock/)

A Retrieval-Augmented Generation (RAG) application built with AWS Bedrock that uses knowledge bases and guardrails to provide secure, contextual responses.

## Features

- **AWS Bedrock Integration**: Leverages AWS Bedrock's knowledge base and LLaMA 3 70B model
- **Guardrails Protection**: Implements AWS Bedrock guardrails for content filtering and safety
- **Vector Search**: Configurable vector search with result limiting
- **Environment-based Configuration**: Secure configuration management using environment variables
- **Lambda-ready**: Designed for AWS Lambda deployment

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS CLI configured or environment variables set
- Access to AWS Bedrock knowledge bases and guardrails

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vashishtavarma/aws-rag.git
   cd aws-rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   KNOWLEDGE_BASE_ID=your_knowledge_base_id
   GUARDRAIL_ID=your_guardrail_id
   GUARDRAIL_VERSION=number
   REGION_NAME=your_region_name
   LLAMA_MODEL_ARN=your_llama_model_arn
   ```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `KNOWLEDGE_BASE_ID` | AWS Bedrock Knowledge Base ID | Yes |
| `GUARDRAIL_ID` | AWS Bedrock Guardrail ID | Yes |
| `GUARDRAIL_VERSION` | Guardrail version (default: 1) | Yes |
| `REGION_NAME` | AWS region | Yes |
| `LLAMA_MODEL_ARN` | LLaMA model ARN | Yes |

### Model Configuration

The application uses the LLaMA 3 70B Instruct model with the following configuration:
- Vector search with configurable result limits
- Guardrail-protected generation
- Knowledge base retrieval integration

## Usage

### Local Testing

Run the application locally for testing:

```bash
python app.py
```

The application will execute a test query and display the response.

### Lambda Deployment

The application is designed as an AWS Lambda function. Deploy it to AWS Lambda and invoke with:

```json
{
  "question": "Your question here"
}
```

### Response Format

The application returns responses in the following format:

```json
{
  "statusCode": 200,
  "body": {
    "question": "Your question",
    "answer": {
      "output": {
        "text": "Generated response"
      }
    }
  }
}
```

## API Reference

### `lambda_handler(event, context)`

Main Lambda function handler.

**Parameters:**
- `event`: Lambda event object containing the question
- `context`: Lambda context object

**Required Event Structure:**
```json
{
  "question": "string"
}
```

### `retrieve_and_generate_with_guardrails(input_text, kbId)`

Core function that handles RAG operations.

**Parameters:**
- `input_text`: The user's question/query
- `kbId`: Knowledge base ID

**Returns:** AWS Bedrock response object

## Security Features

- **Guardrails**: Content filtering and safety measures
- **Environment Variables**: Secure credential management
- **AWS IAM**: Role-based access control
- **Vector Search Filtering**: Controlled result retrieval

## Error Handling

The application handles common errors:
- Missing question in request (400 status)
- AWS authentication errors
- Bedrock service errors
- Invalid configuration

## Development

### Project Structure

```
aws-rag/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .gitignore         # Git ignore rules
├── venv/              # Virtual environment
└── README.md          # This file
```

### Dependencies

- `boto3`: AWS SDK for Python
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **NoRegionError**: Ensure `REGION_NAME` is set in your `.env` file
2. **Authentication Errors**: Verify AWS credentials are correctly configured
3. **Parameter Validation**: Check that all required environment variables are set
4. **Guardrail Responses**: The guardrail may block certain types of content

## License

This project is licensed under the MIT License - see the LICENSE file for details.
