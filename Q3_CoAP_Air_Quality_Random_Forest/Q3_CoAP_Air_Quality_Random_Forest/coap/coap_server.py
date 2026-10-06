import asyncio
import json
import logging
import requests

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.contentformat import ContentFormat

COAP_HOST = "127.0.0.1"
COAP_PORT = 5683

AIR_QUALITY_URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    "?latitude=9.93&longitude=76.27"
    "&current=pm10,pm2_5,nitrogen_dioxide,sulphur_dioxide,ozone"
)


def get_live_air_quality():
    """Fetch current Kochi air-quality data from Open-Meteo."""
    response = requests.get(AIR_QUALITY_URL, timeout=15)
    response.raise_for_status()
    api_data = response.json()

    current = api_data.get("current", {})

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


class AirQualityResource(resource.Resource):
    async def render_get(self, request):
        try:
            # requests is blocking, so execute it outside the asyncio event loop.
            data = await asyncio.to_thread(get_live_air_quality)

            payload = json.dumps(data).encode("utf-8")

            print("\n[CoAP Server] GET /air-quality")
            print("[CoAP Server] Live Kochi data:", data)

            return aiocoap.Message(
                payload=payload,
                content_format=ContentFormat.APPLICATION_JSON
            )

        except Exception as exc:
            error = {"error": str(exc)}
            print("[CoAP Server] Error:", exc)

            return aiocoap.Message(
                code=aiocoap.INTERNAL_SERVER_ERROR,
                payload=json.dumps(error).encode("utf-8"),
                content_format=ContentFormat.APPLICATION_JSON
            )


async def main():
    logging.basicConfig(level=logging.INFO)

    root = resource.Site()
    root.add_resource(
        [".well-known", "core"],
        resource.WKCResource(root.get_resources_as_linkheader)
    )
    root.add_resource(["air-quality"], AirQualityResource())

    await aiocoap.Context.create_server_context(
        root,
        bind=(COAP_HOST, COAP_PORT)
    )

    print("=" * 60)
    print("CoAP Air Quality Server - Kochi")
    print("=" * 60)
    print(f"Listening on coap://{COAP_HOST}:{COAP_PORT}/air-quality")
    print("Waiting for CoAP GET requests...")
    print("Press Ctrl+C to stop.")

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())
