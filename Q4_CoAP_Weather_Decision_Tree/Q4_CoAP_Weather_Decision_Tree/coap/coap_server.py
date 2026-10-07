import asyncio
import json
import logging
import requests

import aiocoap
import aiocoap.resource as resource


# ============================================================
# Q4 - CoAP-Based Weather Monitoring
# Kochi
# ============================================================

COAP_HOST = "127.0.0.1"
COAP_PORT = 5683


# ============================================================
# Open-Meteo Live Weather API
# ============================================================

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=9.93"
    "&longitude=76.27"
    "&current=temperature_2m,relative_humidity_2m,"
    "precipitation,cloud_cover,wind_speed_10m,surface_pressure"
    "&timezone=Asia%2FKolkata"
)


# ============================================================
# Get Live Weather Data
# ============================================================

def get_live_weather():

    response = requests.get(
        WEATHER_URL,
        timeout=15
    )

    # Check API response
    response.raise_for_status()

    api_data = response.json()

    current = api_data.get("current", {})

    # Create clean data for CoAP response
    result = {

        "location": "Kochi",

        "latitude": 9.93,

        "longitude": 76.27,

        "time": current.get("time"),

        "temperature": current.get(
            "temperature_2m"
        ),

        "humidity": current.get(
            "relative_humidity_2m"
        ),

        "precipitation": current.get(
            "precipitation"
        ),

        "cloud_cover": current.get(
            "cloud_cover"
        ),

        "wind_speed": current.get(
            "wind_speed_10m"
        ),

        "surface_pressure": current.get(
            "surface_pressure"
        ),

        "source": "Open-Meteo Weather API"
    }

    return result


# ============================================================
# CoAP Weather Resource
# ============================================================

class WeatherResource(resource.Resource):

    async def render_get(self, request):

        try:

            # Get live weather data
            # without blocking CoAP
            data = await asyncio.to_thread(
                get_live_weather
            )

            # Convert dictionary to JSON
            payload = json.dumps(
                data
            ).encode("utf-8")

            print()
            print(
                "[CoAP Server] GET /weather"
            )

            print(
                "[CoAP Server] Live Kochi weather:",
                data
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Content format 50 = application/json
            #
            # Some versions of aiocoap do NOT have:
            #
            # ContentFormat.APPLICATION_JSON
            #
            # Therefore we use 50 directly.
            # ------------------------------------------------

            return aiocoap.Message(
                payload=payload,
                content_format=50
            )

        except Exception as exc:

            print(
                "[CoAP Server] Error:",
                exc
            )

            error_data = {
                "error": str(exc)
            }

            error_payload = json.dumps(
                error_data
            ).encode("utf-8")

            return aiocoap.Message(

                code=aiocoap.INTERNAL_SERVER_ERROR,

                payload=error_payload,

                content_format=50
            )


# ============================================================
# Start CoAP Server
# ============================================================

async def main():

    logging.basicConfig(
        level=logging.INFO
    )

    # Create CoAP resource tree
    root = resource.Site()

    # CoRE resource discovery
    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(
            root.get_resources_as_linkheader
        )
    )

    # Add weather endpoint
    #
    # CoAP URL:
    # coap://127.0.0.1:5683/weather
    #
    root.add_resource(
        ["weather"],
        WeatherResource()
    )

    # Start CoAP server
    await aiocoap.Context.create_server_context(

        root,

        bind=(
            COAP_HOST,
            COAP_PORT
        )
    )

    print(
        "=" * 60
    )

    print(
        "CoAP Weather Server - Kochi"
    )

    print(
        "=" * 60
    )

    print(
        "Listening on:"
    )

    print(
        f"coap://{COAP_HOST}:{COAP_PORT}/weather"
    )

    print(
        "Waiting for CoAP GET requests..."
    )

    print(
        "Press Ctrl+C to stop."
    )

    # Keep server running
    await asyncio.get_running_loop().create_future()


# ============================================================
# Program Entry Point
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print()
        print(
            "CoAP Weather Server stopped."
        )