import asyncio
import json
import sys

import aiocoap
from aiocoap import GET

COAP_URI = "coap://127.0.0.1:5683/air-quality"


async def get_air_quality():
    protocol = await aiocoap.Context.create_client_context()

    request = aiocoap.Message(
        code=GET,
        uri=COAP_URI
    )

    try:
        response = await protocol.request(request).response

        if not response.code.is_successful():
            raise RuntimeError(f"CoAP request failed: {response.code}")

        data = json.loads(response.payload.decode("utf-8"))
        return data

    finally:
        await protocol.shutdown()


def main():
    try:
        data = asyncio.run(get_air_quality())

        print("=" * 60)
        print("CoAP Client - Received Kochi Air Quality")
        print("=" * 60)
        print(f"Location : {data.get('location')}")
        print(f"Time     : {data.get('time')}")
        print(f"PM2.5    : {data.get('pm2_5')} ug/m3")
        print(f"PM10     : {data.get('pm10')} ug/m3")
        print(f"NO2      : {data.get('no2')} ug/m3")
        print(f"SO2      : {data.get('so2')} ug/m3")
        print(f"O3       : {data.get('o3')} ug/m3")
        print("=" * 60)

        return data

    except Exception as exc:
        print("CoAP Client Error:", exc)
        print("Make sure coap_server.py is running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
