import vertexai
import os

PROJECT_ID = os.environ.get('PROJECT_ID')
LOCATION = os.environ.get('LOCATION')
AGENT_DISPLAY_NAME = os.environ.get('AGENT_DISPLAY_NAME')
AGENT_ID = os.environ.get('AGENT_ID')
STAGING_BUCKET = os.environ.get('BUCKET')

print(f'PROJECT_ID: {PROJECT_ID}')
print(f'LOCATION: {LOCATION}')
print(f'AGENT_DISPLAY_NAME: {AGENT_DISPLAY_NAME}')
print(f'AGENT_ID: {AGENT_ID}')
print(f'STAGING_BUCKET: {STAGING_BUCKET}')

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

from multi_tool_agent.agent import root_agent

from vertexai.preview import reasoning_engines

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

from vertexai import agent_engines

if not AGENT_ID:
    remote_agent = agent_engines.create(
        app,
        requirements=['google-cloud-aiplatform[agent_engines,adk]'],
        display_name=AGENT_DISPLAY_NAME,
        extra_packages=[
            './multi_tool_agent/'
        ],
    )
else:
    remote_agent = agent_engines.update(
        resource_name=AGENT_ID,
        agent_engine=app,
        requirements=['google-cloud-aiplatform[agent_engines,adk]'],
        display_name=AGENT_DISPLAY_NAME,
        extra_packages=[
            './multi_tool_agent/'
        ],
    )
