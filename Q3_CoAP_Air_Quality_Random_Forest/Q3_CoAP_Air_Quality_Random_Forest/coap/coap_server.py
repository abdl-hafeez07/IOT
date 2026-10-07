import asyncio
import json
import logging
import requests

import aiocoap
import aiocoap.resource as resource


# ============================================================
# Q3 - CoAP-Based Air Quality Monitoring
# ESP32/IoT Practical - Kochi
# ============================================================

COAP_HOST = "127.0.0.1"
COAP_PORT = 5683

# Open-Meteo Air Quality API for Kochi
AIR_QUALITY_URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    "?latitude=9.93"
    "&longitude=76.27"
    "&current=pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,ozone"
)


# ============================================================
# Get live air-quality data from Open-Meteo
# ============================================================

def get_live_air_quality():

    response = requests.get(
        AIR_QUALITY_URL,
        timeout=15
    )

    # Check whether API request was successful
    response.raise_for_status()

    api_data = response.json()

    current = api_data.get("current", {})

    # Create clean JSON data for CoAP client
    result = {
        "location": "Kochi",
        "latitude": 9.93,
        "longitude": 76.27,

        "time": current.get("time"),

        "pm2_5": current.get("pm2_5"),
        "pm10": current.get("pm10"),

        "no2": current.get("nitrogen_dioxide"),
        "so2": current.get("sulphur_dioxide"),
        "o3": current.get("ozone"),

        "source": "Open-Meteo Air Quality API"
    }

    return result


# ============================================================
# CoAP Resource
# ============================================================

class AirQualityResource(resource.Resource):

    async def render_get(self, request):

        try:

            # Get live data without blocking the asyncio server
            data = await asyncio.to_thread(
                get_live_air_quality
            )

            # Convert Python dictionary to JSON
            payload = json.dumps(data).encode("utf-8")

            print()
            print("[CoAP Server] GET /air-quality")
            print(
                "[CoAP Server] Live Kochi data:",
                data
            )

            # Content-Format 50 = application/json
            #
            # We use 50 instead of:
            # ContentFormat.APPLICATION_JSON
            #
            # because some aiocoap versions do not provide
            # APPLICATION_JSON as an attribute.
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

    # CoRE Link Format discovery
    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(
            root.get_resources_as_linkheader
        )
    )

    # Create:
    # coap://127.0.0.1:5683/air-quality
    root.add_resource(
        ["air-quality"],
        AirQualityResource()
    )

    # Start CoAP server
    await aiocoap.Context.create_server_context(
        root,
        bind=(
            COAP_HOST,
            COAP_PORT
        )
    )

    print("=" * 60)
    print("CoAP Air Quality Server - Kochi")
    print("=" * 60)

    print(
        "Listening on:"
    )

    print(
        f"coap://{COAP_HOST}:{COAP_PORT}/air-quality"
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
        print("CoAP Server stopped.")