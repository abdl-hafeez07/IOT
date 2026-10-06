import asyncio
import json
import logging
import requests

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat

COAP_HOST = "127.0.0.1"
COAP_PORT = 5683

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=9.93&longitude=76.27"
    "&current=temperature_2m,relative_humidity_2m,precipitation,"
    "cloud_cover,wind_speed_10m,surface_pressure"
    "&timezone=Asia%2FKolkata"
)


def get_live_weather():
    response = requests.get(WEATHER_URL, timeout=15)
    response.raise_for_status()

    api_data = response.json()
    current = api_data.get("current", {})

    return {
        "location": "Kochi",
        "latitude": 9.93,
        "longitude": 76.27,
        "time": current.get("time"),
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "precipitation": current.get("precipitation"),
        "cloud_cover": current.get("cloud_cover"),
        "wind_speed": current.get("wind_speed_10m"),
        "surface_pressure": current.get("surface_pressure"),
        "source": "Open-Meteo Weather API"
    }


class WeatherResource(resource.Resource):
    async def render_get(self, request):
        try:
            data = await asyncio.to_thread(get_live_weather)
            payload = json.dumps(data).encode("utf-8")

            print("\n[CoAP Server] GET /weather")
            print("[CoAP Server] Live Kochi weather:", data)

            return aiocoap.Message(
                payload=payload,
                content_format=ContentFormat.APPLICATION_JSON
            )

        except Exception as exc:
            print("[CoAP Server] Error:", exc)

            return aiocoap.Message(
                code=aiocoap.INTERNAL_SERVER_ERROR,
                payload=json.dumps({"error": str(exc)}).encode("utf-8"),
                content_format=ContentFormat.APPLICATION_JSON
            )


async def main():
    logging.basicConfig(level=logging.INFO)

    root = resource.Site()
    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(root.get_resources_as_linkheader)
    )
    root.add_resource(["weather"], WeatherResource())

    await aiocoap.Context.create_server_context(
        root,
        bind=(COAP_HOST, COAP_PORT)
    )

    print("=" * 60)
    print("CoAP Weather Server - Kochi")
    print("=" * 60)
    print(f"Listening on coap://{COAP_HOST}:{COAP_PORT}/weather")
    print("Waiting for CoAP GET requests...")
    print("Press Ctrl+C to stop.")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
