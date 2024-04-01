import aiohttp
from loguru import logger


class Client:

    def __init__(self, dolphin_token=None):
        self.token = dolphin_token

    @staticmethod
    async def get_ads_profile_ids_async() -> list | None:
        ads_profiles = []
        payload = {'page_size': 100}
        url = 'http://local.adspower.net:50325/api/v1/user/list'
        data = None
        async with aiohttp.ClientSession() as session:
            r = await session.get(url, params=payload)
            if r.status == 200:
                data = await r.json()
            if data:
                if data['data']:
                    if data['data']['list']:
                        for item in data['data']['list']:
                            ads_profiles.append(item['user_id'])
        return ads_profiles if len(ads_profiles) > 0 else None

    async def list_profile_ids_dolphin(self) -> list:
        id_list = []
        headers = {'Authorization': f'Bearer {self.token}',
                   'Content-Type': 'application/json'}
        try:
            authorized = await self.token_auth_dolphin_async()
            if authorized:
                logger.success(f'Authorized user by token {self.token[:3]}...'
                               f'{self.token[len(self.token) - 3: len(self.token)]}, getting profile ids')
        except Exception:
            pass
        for i in range(1, 10):
            async with aiohttp.ClientSession() as session:
                url = f'https://dolphin-anty-api.com/browser_profiles?limit=50&page={i}'
                session.headers.update(headers)
                r = await session.get(url)
                if r.status == 200:
                    resp = await r.json()
                    ids = resp['data']
                    if len(ids) > 0:
                        id_list.extend(ids)
                    else:
                        break
                else:
                    logger.error(f'Bad request - {r.status} - {r.text}')
        return id_list

    async def token_auth_dolphin_async(self) -> bool:
        logger.debug(
            f'Trying to authenticate with token {self.token[:3]}...{self.token[len(self.token) - 3: len(self.token)]}')
        url = 'http://localhost:3001/v1.0/auth/login-with-token'

        data = {
            'token': self.token
        }

        try:
            async with aiohttp.ClientSession() as session:
                session.headers.update({'Content-Type': 'application/json'})
                r = await session.post(url, json=data)
                if r.status == 200:
                    resp = await r.json()
                    return True if resp['success'] else False
                elif r.status == 500:
                    return True
                else:
                    return False
        except Exception as e:
            logger.error(e)
