from google.adk.agents import Agent
from .tools import get_detail_by_google_map

def create():
    agent = Agent(
        name="trip_itinerary_agent",
        model="gemini-2.5-flash",
        description="Agent to generate itinerary.",
        instruction="""You are an itinerary generator. Please respond with a title for this trip and a detailed timetable. The output must follow the schema below:

{
    title: "string",
    activities: [
        {
            type: "sightseeing, restaurant, shopping, accommodation, freeTime, transport, other",
            location: "string",
            "startTimeUtc": "2025-09-06T07:00:00Z",
            "endTimeUtc": "2025-09-06T07:00:00Z",
            "timeZone": "Europe/Paris",
            duration: "minutes",
            transportType: "train, highSpeedTrain, flight, bus, taxi, bike, walk, car, boat, motorcycle, other",
            note: "string",
            placeUri: "string",
            latLng: {
                latitude: double,
                longitude: double,
            },
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
- Use the RFC 3339 time format without a timezone offset.
- Fill in the timeZone for the location to be visited.
- All keys must be present and correctly spelled.
- Retrieve the values of "latLng" and "placeUri" using the get_detail_by_google_map tool.
        """,
        tools=[get_detail_by_google_map],
    )
    return agent
