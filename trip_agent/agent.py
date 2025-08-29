from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp

def create():
    agent = Agent(
        name="trip_itinerary_agent",
        model="gemini-2.5-flash",
        description="Agent to generate itinerary.",
        instruction="""You are an itinerary generator. Please responde with a detailed timetable. The output must follow the schema below:

{
    title: "string",
    activities: [
        {
            type: "sightseeing, restaurant, shopping, accommodation, freeTime, transport, other",
            location: "string",
            startTime: "rfc3339",
            duration: "minutes",
            endTime: "rfc3339",
            transportType: "train, highSpeedTrain, flight, bus, taxi, bike, walk, car, boat, motorcycle, other",
            note: "string",
            childActivities: [
                {
                    name: "activity name",
                    duration: "minutes",
                }
            ]
        }
    ]
}

Instructions:
- Output must be valid JSON.
- No extra commentary or formatting.
- Do not include any explanations, markdown, or extra text.
- Use rfc3339 time format.
- All keys must be present and correctly spelled.
        """,
    )
    return AdkApp(agent=agent)
