import asyncio
import json
import sys

import aiocoap
from aiocoap import GET

COAP_URI = "coap://127.0.0.1:5683/weather"


async def get_weather():
    protocol = await aiocoap.Context.create_client_context()

    request = aiocoap.Message(
        code=GET,
        uri=COAP_URI
    )

    try:
        response = await protocol.request(request).response

        if not response.code.is_successful():
            raise RuntimeError(f"CoAP request failed: {response.code}")

        return json.loads(response.payload.decode("utf-8"))

    finally:
        await protocol.shutdown()


def main():
    try:
        data = asyncio.run(get_weather())

        print("=" * 60)
        print("CoAP Client - Received Kochi Weather")
        print("=" * 60)
        print(f"Location          : {data.get('location')}")
        print(f"Time              : {data.get('time')}")
        print(f"Temperature       : {data.get('temperature')} °C")
        print(f"Relative Humidity : {data.get('humidity')} %")
        print(f"Precipitation     : {data.get('precipitation')} mm")
        print(f"Cloud Cover       : {data.get('cloud_cover')} %")
        print(f"Wind Speed        : {data.get('wind_speed')} km/h")
        print(f"Surface Pressure  : {data.get('surface_pressure')} hPa")
        print("=" * 60)

    except Exception as exc:
        print("CoAP Client Error:", exc)
        print("Make sure coap_server.py is running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
