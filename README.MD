# Twitter Archive Downloader

The Twitter Archive Downloader is a Python utility for scraping and downloading tweets from specific Twitter accounts or statuses. It uses asynchronous HTTP requests to efficiently download tweets and saves them in text or JSON format.

## Features

- Asynchronous downloading of tweets using `aiohttp`.
- Logging with customizable color-coded output for different log levels.
- Command-line argument support for dynamic scraping.
- Data extraction using `BeautifulSoup` for parsing HTML content.
- Saving data in text and JSON formats.

## Requirements

- Python 3.6+
- `aiohttp`, `beautifulsoup4`, `requests`, `colorama`
- An environment that supports ANSI escape codes for colored logging.

## Installation

Before running the script, ensure you have the required packages:

```bash
pip install aiohttp beautifulsoup4 requests colorama
```

## Usage

To use the Twitter Archive Downloader, you should provide the base URL as an argument:

```bash
python twitter_archive_downloader.py https://twitter.com/elonmusk/*
```

Replace the URL with the specific Twitter status or account you're interested in downloading.

## How It Works

1. **Initialization**: Configure the logger and create an instance of the downloader with the provided base URL.
2. **Fetching URLs**: Use the Wayback Machine API to retrieve archived tweets URLs.
3. **Downloading and Processing**: Asynchronously download and process each tweet, extracting the content.
4. **Saving Results**: Save the extracted tweets into text or JSON files for later use or analysis.

## Customization

- Modify log level and format by adjusting the `logging` setup.
- Change the number of maximum concurrent requests to optimize performance based on your system and network capabilities.

## Note

This script is meant for educational purposes and should be used responsibly. Ensure you are compliant with Twitter's terms of service and applicable laws regarding scraping and data usage.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/omeh2003/twitter_archive_downloader/issues) if you want to contribute.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [omeh2003@gmail.com](mailto:omeh2003@gmail.com)

Project Link: [https://github.com/omeh2003/twitter_archive_downloader](https://github.com/omeh2003/twitter_archive_downloader)
```

This README provides a basic outline for your project, including how to install, run, and understand the basic functionality of your Twitter Archive Downloader script. You should customize the "Contact" and "Contributing" sections with your own information, and ensure that the "License" section accurately reflects how you wish to distribute your code. Additionally, replace the placeholder URLs with the actual URL to your repository once you have created it.