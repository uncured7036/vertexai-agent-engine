from google.adk.agents import Agent
from .tools import get_detail_by_google_map
from .tools import get_candidate_places_by_google_map

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
- The JSON should begin with `STARTJSON` and end with "ENDJSON".
- Please confirm and explain any modification, unless I've explicitly instructed you to output the JSON directly.'
- The time is based on the timezone of the visited location and should be formatted using RFC 3339, then converted to UTC..
- Fill in the timeZone for the location to be visited.
- All keys must be present and correctly spelled.
- Retrieve the values of "latLng" and "placeUri" using the get_detail_by_google_map tool.
- Each activity should be assigned to a specific place. You can retrieve candidate locations using the get_candidate_places_by_google_map tool, which takes the location name and activity type as inputs.
- The activity type must be one of the following: sightseeing, restaurant, shopping, accommodation, freeTime, transport, or other.
- The transportType must be one of the following: train, highSpeedTrain, flight, bus, taxi, bike, walk, car, boat, motorcycle, or other
- Please ensure that the each activity has the continuous time slot. Use `freeTime` to fill any gaps and prevent empty activity slots.
- Consolidate activities into childActivities when their lantitude and longitude are the same.
- Trim the location name to a maximum 10 words.
- If the activity location is not a specific place, leave the `placeUri` and `latLng` fields empty.
        """,
        tools=[get_detail_by_google_map, get_candidate_places_by_google_map],
    )
    return agent
