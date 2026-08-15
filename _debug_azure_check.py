import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
endpoint = os.getenv('AZURE_ENDPOINT', '').strip().rstrip('/')
if '/api/projects/' in endpoint:
    endpoint = endpoint.split('.services.ai.azure.com', 1)[0] + '.openai.azure.com'
key = os.getenv('AZURE_API_KEY', '')
deployment = os.getenv('AZURE_DEPLOYMENT', '')
print('HAS_ENDPOINT', bool(endpoint))
print('HAS_KEY', bool(key))
print('HAS_DEPLOYMENT', bool(deployment))
client = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version='2024-10-21')
try:
    resp = client.chat.completions.create(
        model=deployment,
        messages=[{'role': 'user', 'content': 'hi'}],
        max_tokens=20,
    )
    print('RESULT_OK', bool(resp.choices and resp.choices[0].message and resp.choices[0].message.content))
except Exception as e:
    print('EXCEPTION_TYPE', type(e).__name__)
    print('EXCEPTION_MESSAGE', str(e)[:200])
