import vertexai
import os

PROJECT_ID = os.environ.get('_PROJECT_ID')
LOCATION = os.environ.get('_LOCATION')
AGENT_DISPLAY_NAME = os.environ.get('_AGENT_DISPLAY_NAME')
AGENT_ID = os.environ.get('_AGENT_ID')
STAGING_BUCKET = os.environ.get('_BUCKET')

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
