import asyncio
import json
from utils.get_data_path import get_data_path
from loguru import logger
from config import DOLPHIN_SESSIONS
from tasks.web3go import Web3Go
from tasks.starrynift import StarryNift

path = get_data_path()
user_data_json = json.load(open(path))
dolphin_auth_key = user_data_json[0]['dolphin_auth_key']


tasks = {
    1: 'Web3Go',
    2: 'StarryNift'
}


async def main():
    logger.debug('Enter the number of the task:\n1.Web3Go\n2.StarryNift')
    task_input = int(input())
    match(task_input):
        case 1:
            task = Web3Go(
                dolphin_token=dolphin_auth_key if DOLPHIN_SESSIONS else None)
            await task.perform_daily_async()
        case 2:
            task = StarryNift(
                dolphin_token=dolphin_auth_key if DOLPHIN_SESSIONS else None)
            await task.perform_daily_async()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug('Program closed')
