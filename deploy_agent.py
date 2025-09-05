import vertexai
import os

PROJECT_ID = os.environ.get('PROJECT_ID')
LOCATION = os.environ.get('LOCATION')
AGENT_DISPLAY_NAME = os.environ.get('AGENT_DISPLAY_NAME')
AGENT_ID = os.environ.get('AGENT_ID')
STAGING_BUCKET = os.environ.get('BUCKET')

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

import trip_agent

from vertexai.preview import reasoning_engines

app = reasoning_engines.AdkApp(
    agent=trip_agent.create(),
    enable_tracing=True,
)

from vertexai import agent_engines

if not AGENT_ID:
    remote_agent = agent_engines.create(
        app,
        requirements=[
            'cloudpickle==3.1.1',
            'pydantic==2.11.7',
            'google-cloud-aiplatform[agent_engines,adk]==1.110.0',
        ],
        display_name=AGENT_DISPLAY_NAME,
        extra_packages=[
            './trip_agent/'
        ],
        #container_concurrency=5,
    )
else:
    remote_agent = agent_engines.update(
        resource_name=AGENT_ID,
        agent_engine=app,
        requirements=[
            'cloudpickle==3.1.1',
            'pydantic==2.11.7',
            'google-cloud-aiplatform[agent_engines,adk]==1.110.0',
        ],
        display_name=AGENT_DISPLAY_NAME,
        extra_packages=[
            './trip_agent/'
        ],
        #container_concurrency=5,
    )
