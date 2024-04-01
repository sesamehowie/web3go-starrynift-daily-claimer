import json
from asyncio import sleep
from random import randint
import aiohttp
from loguru import logger
from playwright.async_api import async_playwright, expect
from client import Client
from config import ADS_SESSIONS, DOLPHIN_SESSIONS

# json absolute path
path = ''

INFO_JSON = json.load(open(path))


class StarryNift(Client):

    def __init__(self, dolphin_token):
        super().__init__(dolphin_token)
        self.token = dolphin_token

    @staticmethod
    async def setup_context(context):
        context.set_default_navigation_timeout(20000)
        context.set_default_timeout(25000)
        await sleep(randint(8, 10))
        page = await context.new_page()
        while len(context.pages) > 1:
            unneeded_page = context.pages[0]
            await unneeded_page.close()
        return page

    @staticmethod
    async def metamask_auth(page, password):
        await page.goto('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock')
        await page.wait_for_load_state()
        await expect(page.locator('//*[@id="password"]')).to_be_visible()
        await page.locator('//*[@id="password"]').fill(password, force=True)
        await expect(page.locator('//*[@id="app-content"]/div/div[2]/div/div/button')).to_be_visible()
        await page.locator('//*[@id="app-content"]/div/div[2]/div/div/button').click(force=True)
        await page.wait_for_load_state()
        await expect(page.locator('//*[@id="app-content"]/div/div[2]/div/div[2]/div/div/button/span')).to_be_visible()
        if not any([elem in await page.locator(
                '//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]').text_content() for elem in
                ['BNB Chain', 'ANKR', 'Binance Smart Chain', 'BSC']]):
            await page.locator('//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]').click(force=True)
            await page.wait_for_load_state()
            if await page.get_by_text('ANKR').is_visible():
                await page.get_by_text('ANKR').click(force=True)
                await page.wait_for_load_state()
            elif await page.get_by_text('BNB Chain').is_visible():
                await page.get_by_text('BNB Chain').click(force=True)
                await page.wait_for_load_state()
            elif await page.get_by_text('Binance Smart Chain').is_visible():
                await page.get_by_text('Binance Smart Chain').click(force=True)
                await page.wait_for_load_state()
            elif await page.get_by_text('BSC').is_visible():
                await page.get_by_text('BSC').click(force=True)
                await page.wait_for_load_state()
            else:
                await expect(
                    page.locator('//html/body/div[3]/div[3]/div/section/div[1]/div[2]/button/span')).to_be_visible()
                await page.locator('//html/body/div[3]/div[3]/div/section/div[1]/div[2]/button/span').click(force=True)
                await page.locator('//*[@id="app-content"]/div/div[2]/div/div[2]/div/div/button/span').click(force=True)
                await expect(page.locator('//*[@id="popover-content"]/div[2]/button[6]/div/div')).to_be_visible()
                await page.locator('//*[@id="popover-content"]/div[2]/button[6]/div/div').click(force=True)
                await page.wait_for_load_state()
                if page.url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings':
                    await expect(page.locator(
                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[1]/div/button[6]/div')).to_be_visible()
                    await page.locator('//*[@id="app-content"]/div/div[3]/div/div[2]/div[1]/div/button[6]/div').click(
                        force=True)
                    await page.wait_for_load_state()
                    if page.url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks':
                        if not any([elem in await page.locator(
                                    '//*[@id="app-content"]/div/div[2]/div/div[1]/button/span[1]').text_content() for elem
                                    in
                                    ['BNB Chain', 'ANKR', 'Binance Smart Chain']]):
                            await expect(page.locator(
                                '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[1]/div/button')).to_be_visible()
                            await page.locator(
                                '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[1]/div/button').click(
                                force=True)
                            await page.wait_for_load_state()
                            if page.url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks/add-popular-custom-network':
                                await expect(page.locator(
                                    '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[3]/a/h6')).to_be_visible()
                                await page.locator(
                                    '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[3]/a/h6').click(
                                    force=True)
                                await page.wait_for_load_state()
                                if page.url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks/add-network':
                                    await expect(page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input')).to_be_visible()
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input').fill(
                                        'BNB Chain', force=True)
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input').fill(
                                        'https://bsc.meowrpc.com', force=True)
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input').fill(
                                        '56', force=True)
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/div/input').fill(
                                        'BNB', force=True)
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/label/input').fill(
                                        'https://bscscan.com/', force=True)
                                    await expect(page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')).to_be_visible()
                                    await page.locator(
                                        '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]').click(
                                        force=True)
                                    await page.wait_for_load_state()
                                    if page.url == 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#':
                                        await expect(page.locator(
                                            '//*[@id="popover-content"]/div/div/section/div[2]/div/button[1]/h6')).to_be_visible()
                                        await page.locator(
                                            '//*[@id="popover-content"]/div/div/section/div[2]/div/button[1]/h6').click(
                                            force=True)

    async def claim_daily(self, browser, password):
        context = browser.contexts[0]
        page = await self.setup_context(context)
        await self.metamask_auth(page, password=password)
        await page.goto('https://starrynift.art/')
        await page.wait_for_load_state()
        await page.reload()
        await page.wait_for_load_state()
        await expect(page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div')).to_be_visible()
        await page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div/div').click(force=True)
        await expect(page.get_by_text('MetaMask')).to_be_visible()
        async with context.expect_page() as new_page_info:
            await page.get_by_text('MetaMask').click(force=True)
        mm_noti = await new_page_info.value
        await mm_noti.wait_for_load_state()
        await expect(mm_noti.locator('//html/body/div[1]/div/div/div/div[4]/footer/button[2]')).to_be_visible()
        await mm_noti.locator('//html/body/div[1]/div/div/div/div[4]/footer/button[2]').click(force=True)
        await page.wait_for_load_state()
        await page.wait_for_timeout(10000)
        await page.wait_for_load_state()
        await expect(page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div[5]/div')).to_be_visible(timeout=35000)
        await page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div[5]/div').click(force=True)
        await page.wait_for_load_state()
        if page.url == 'https://starrynift.art/earn':
            await expect(page.locator('//html/body/div/div/div/div[1]/div[3]/div/div[2]/div[1]/div[2]/button/span')).to_be_visible(timeout=60000)
            await page.locator('//html/body/div/div/div/div[1]/div[3]/div/div[2]/div[1]/div[2]/button/span').click(force=True)
        await expect(page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/img')).to_be_visible()
        await page.locator('//html/body/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/img').hover()
        await expect(page.get_by_text('Disconnect')).to_be_visible()
        await page.get_by_text('Disconnect').click(force=True)
        await page.wait_for_load_state()
        await context.clear_cookies()
        await context.clear_permissions()
        await context.close()

    async def perform_daily_async(self):
        if DOLPHIN_SESSIONS:
            profile_ids = await self.list_profile_ids_dolphin()
            if profile_ids:
                for dolph_id in profile_ids:
                    browser_id = dolph_id['id']
                    browser_name = dolph_id['name']
                    for item in INFO_JSON[0]['dolphin']:
                        if browser_name in item['profile_names']:
                            password = item['metamask_pass']
                            break
                    else:
                        password = None
                    if password:
                        logger.debug('Profile ids intact, proceeding')
                        async with aiohttp.ClientSession() as session:
                            url = f'http://localhost:3001/v1.0/browser_profiles/{browser_id}/start?automation=1'
                            session.headers.update({'Authorization': f'Bearer {self.token}',
                                                    })
                            r = await session.get(url)
                            if r.status == 200:
                                resp = await r.json()
                                port = resp['automation']['port']
                                ws_endpoint = resp['automation']['wsEndpoint']
                            else:
                                logger.error(f'{r.status} -- {r.text}')
                            if port and ws_endpoint:
                                async with async_playwright() as p:
                                    chromi = p.chromium
                                    browser = await chromi.connect_over_cdp(f'ws://127.0.0.1:{port}{ws_endpoint}')
                                    await self.claim_daily(browser, password)
                                    url = f'http://localhost:3001/v1.0/browser_profiles/{browser_id}/stop'
                                    await session.get(url)
                                    await session.close()
        elif ADS_SESSIONS:
            profile_ids = await self.get_ads_profile_ids_async()
            if profile_ids:
                for ads_id in profile_ids:
                    for item in INFO_JSON[0]['ads']:
                        if ads_id == item['profile_id']:
                            password = item['metamask_pass']
                            break
                    else:
                        password = None
                    if password:
                        async with aiohttp.ClientSession() as session:
                            open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
                            close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id
                            r = await session.get(open_url)
                            if r.status == 200:
                                data = await r.json()
                                ws_endpoint = data['data']['ws']['puppeteer']
                            else:
                                logger.error(f'{r.status} -- {r.text}')
                            if ws_endpoint:
                                async with async_playwright() as p:
                                    chromi = p.chromium
                                    browser = await chromi.connect_over_cdp(ws_endpoint)
                                    await self.claim_daily(browser, password)
                                    await session.get(close_url)
                                    await session.close()
