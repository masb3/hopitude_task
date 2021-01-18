import asyncio

import aiohttp
from django.db.utils import IntegrityError

from core.models import IotDeviceData


BASE_URL = 'https://jsonmock.hackerrank.com/api/iot_devices/'


async def async_main(requests):
    async with aiohttp.ClientSession() as session:
        tasks = [async_get_url_json(session, url=request) for request in requests]
        return await asyncio.gather(*tasks)


async def async_get_url_json(session, url):
    async with session.get(url) as resp:
        if resp.status == 200:
            resp_json = await resp.json()
            return resp_json
        return None


def fetch_new_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Initial request
    results = loop.run_until_complete(async_main([BASE_URL]))

    # Fetch more pages if any and extend results
    if results:
        curr_page = int(results[0].get('page'))
        total_pages = int(results[0].get('total_pages'))
        urls = []
        for page in range(curr_page+1, total_pages+1):
            urls.append(BASE_URL+f'?page={page}')
        results.extend(loop.run_until_complete(async_main(urls)))

        for result in results:
            for data in result.get('data'):
                try:  # Save to DB only if data_id is not yet stored
                    parent = data.get('parent')
                    parent_id = None if not parent else parent.get('id')
                    parent_alias = None if not parent else parent.get('alias')
                    IotDeviceData.objects.create(data_id=data.get('id'),
                                                 timestamp=data.get('timestamp'),
                                                 status=data.get('status'),
                                                 rotor_speed=data.get('operatingParams').get('rotorSpeed'),
                                                 slack=data.get('operatingParams').get('slack'),
                                                 root_threshold=data.get('operatingParams').get('rootThreshold'),
                                                 asset_id=data.get('asset').get('id'),
                                                 asset_alias=data.get('asset').get('alias'),
                                                 parent_id=parent_id,
                                                 parent_alias=parent_alias
                                                 )
                except IntegrityError:
                    pass

    loop.close()







