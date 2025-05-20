# Steam Deck Refurbished Stock Checker

## Description

This project provides a script to monitor the availability of refurbished Steam Deck units on the official store page and send a notification to a specified Discord channel when stock is detected. The script uses Selenium for web scraping and a Discord webhook for notifications.

## Prerequisites

Before using this script, ensure the following dependencies are installed:

1. Python 3 
2. Selenium and Requests Python packages (specified in requirements.txt)
    ```sh
    pip install -r requirements.txt
    ```

## Setup Instructions

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd steam-deck-stock-checker
    ```
2. Set up your Discord Webhook URL:
    - Create a python file called *env.py* and place your Discord Webhook URL in a string var. called **DISCORD_WEBHOOK_URL**
    - In checker.py, replace the placeholder webhook_url with your imported string from *env.py*:
    ```python
    webhook_url = DISCORD_WEBHOOK_URL
    ```
3. Set permissions and scheduling:
    - Ensure `script.sh` is executable:
    ```sh
    chmod +x script.sh
    ```
    - Add `script.sh` to a cron job to check for stock periodically (every 5 minutes in this example):
    ```sh
    */5 * * * * /bin/bash /path/to/steam-deck-stock-checker/script.sh
    ```

## Disclaimer

This script is provided "as is" for personal use. Be aware of website scraping policies and use responsibly.