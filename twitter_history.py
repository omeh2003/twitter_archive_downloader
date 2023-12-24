import aiohttp
import asyncio
import requests
import json
import os
import logging
from bs4 import BeautifulSoup
import logging
import sys
from colorama import Fore, Style, init
import argparse


init(autoreset=True)


class CustomFormatter(logging.Formatter):

    def format(self, record):
        color = ''
        if record.levelno == logging.INFO:
            color = Fore.BLUE
        elif record.levelno == logging.WARNING:
            color = Fore.YELLOW
        elif record.levelno == logging.ERROR:
            color = Fore.RED
        formatted_record = super().format(record)
        return f"{color}{formatted_record}{Style.RESET_ALL}"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.handlers = [handler]


def emit_override(record):
    try:
        msg = handler.format(record)
        if record.levelno == logging.INFO:
            sys.stdout.write('\033[K' + msg + '\r')
        else:
            sys.stdout.write(msg + '\n')
        sys.stdout.flush()
    except Exception:
        handler.handleError(record)


handler.emit = emit_override

logger.info("Это будет перезаписано")
import time


time.sleep(1)
logger.info("Первое информационное сообщение")
time.sleep(1)
logger.warning("Предупреждение")
logger.info("Второе информационное сообщение")
time.sleep(1)
logger.error("Ошибка")
logger.info("Третье информационное сообщение")

DIRECTORY = './data/'
MAX_CONCURRENT_REQUESTS = 2


class TwitterArchiveDownloader:

    def __init__(self, base_url, max_concurrent_requests):
        self.base_url = base_url
        self.max_concurrent_requests = max_concurrent_requests
        self.text_data = ""
        self.json_data = []

    async def fetch_url(self, session, url):
        count = 0
        while count < 5:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        logger.info(f"Successfully fetched URL {url[42:]}")
                        return await response.text()
            except Exception as e:
                logger.error(f"Exception fetching URL {url}: {e}")
                # Be cautious with recursive retries, consider implementing a max retry limit
                count += 1
        logger.warning(f"Failed to fetch URL {url}")
        return None

    async def process_content(self, url, content):
        if content:
            if content.lstrip().startswith('<'):  # HTML
                self.text_data += self.extract_tweets(content)
                logger.info(f"Processed HTML content from {url[42:]}")
            else:  # JSON
                try:
                    data = json.loads(content)
                    self.json_data.append(data)
                    logger.info(f"Processed JSON content from {url[42:]}")
                except json.JSONDecodeError:
                    logger.warning(f"Failed to decode JSON from {url[42:]}")

    async def download_and_process_url(self, session, url):
        content = await self.fetch_url(session, url)
        await self.process_content(url, content)

    async def bulk_download_and_process(self, urls):
        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(self.max_concurrent_requests)
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.download_and_process_url(session, url))
                tasks.append(task)
                await semaphore.acquire()
                task.add_done_callback(lambda t: semaphore.release())
            await asyncio.gather(*tasks)

    def get_wayback_urls(self):
        try:
            cdx_url = f"http://web.archive.org/cdx/search/cdx?url={self.base_url}&output=json&fl=original,timestamp"
            response = requests.get(cdx_url)
            records = json.loads(response.text)
            logger.info("Successfully retrieved wayback URLs")
            return [f"http://web.archive.org/web/{timestamp}/{original}" for original, timestamp in records[1:]]
        except Exception as e:
            logger.error(f"Failed to retrieve wayback URLs: {e}")
            return []

    def extract_tweets(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        classes = ["js-tweet-text tweet-text", "js-tweet-text-container"]
        tweets = sum((soup.find_all(class_=class_name) for class_name in classes), [])
        return '\n'.join(tweet.get_text(strip=True) for tweet in tweets)

    def save_results(self):
        if self.text_data:
            with open('combined_txt2.txt', 'w', encoding='utf-8') as text_file:
                text_file.write(self.text_data)
            logger.info("Text data saved to combined_txt2.txt")

        if self.json_data:
            with open('combined_json2.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.json_data, json_file, ensure_ascii=False, indent=4)
            logger.info("JSON data saved to combined_json2.json")

    def run(self):
        urls = self.get_wayback_urls()
        asyncio.run(self.bulk_download_and_process(urls))
        self.save_results()
        logger.info("Finished downloading and processing all URLs.")


if __name__ == "__main__":
    # Создаем парсер и определяем аргумент BASE_URL
    BASE_URL = "https://twitter.com/elonmusk/*"
    parser = argparse.ArgumentParser(description="Twitter Archive Downloader")
    parser.add_argument("base_url", help="Base URL to scrape example: https://twitter.com/elonmusk/* ")
    args = parser.parse_args()

    # Теперь используем BASE_URL из командной строки
    downloader = TwitterArchiveDownloader(args.base_url, MAX_CONCURRENT_REQUESTS)
    downloader.run()
