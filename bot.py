import os
import requests
from datetime import datetime
import pytz
from telegram import Bot
from telegram.error import TelegramError

# --- اطلاعات محرمانه ربات و کانال شما ---
# این اطلاعات از ورودی شما گرفته شده است.
BOT_TOKEN = "8474833531:AAFLMru05yIvtWgvUQXyMi-GlHqLD7h7vYM"
CHANNEL_ID = "@elctronicmosic"
MESSAGE_ID = 132

# --- تنظیمات ارزها ---
COIN_IDS = [
    'bitcoin', 'ethereum', 'solana', 'binancecoin', 'ripple',
    'dogecoin', 'cardano', 'tron', 'shiba-inu', 'the-open-network'
]

# --- قالب پیام پین شده ---
MESSAGE_TEMPLATE = """
📊 تابلو زنده کریپتو | آپدیت خودکار ساعتی

🗺 قیمت لحظه‌ای رمزارزهای مهم:
(آپدیت ساعتی)

😀 BTC: {btc:,.0f}
😀 ETH: {eth:,.2f}
🪙 SOL: {sol:,.2f}
🪙 BNB: {bnb:,.2f}
🪙 XRP: {xrp:,.4f}
🪙 DOGE: {doge:,.4f}
🪙 ADA: {ada:,.4f}
🪙 TRX: {trx:,.4f}
🪙 SHIB: {shib:,.8f}
🪙 TON: {ton:,.2f}

📒 آخرین آپدیت: {update_time}

⚓️ این پست همیشه در بالای کانال پین می‌مونه و به‌طور خودکار آپدیت می‌شه.
📱@elctronicmosic
"""

def get_crypto_prices():
    """از API سایت CoinGecko قیمت‌ها را درخواست می‌کند."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(COIN_IDS)}&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        prices = response.json()
        return {
            'btc': prices.get('bitcoin', {}).get('usd', 0),
            'eth': prices.get('ethereum', {}).get('usd', 0),
            'sol': prices.get('solana', {}).get('usd', 0),
            'bnb': prices.get('binancecoin', {}).get('usd', 0),
            'xrp': prices.get('ripple', {}).get('usd', 0),
            'doge': prices.get('dogecoin', {}).get('usd', 0),
            'ada': prices.get('cardano', {}).get('usd', 0),
            'trx': prices.get('tron', {}).get('usd', 0),
            'shib': prices.get('shiba-inu', {}).get('usd', 0),
            'ton': prices.get('the-open-network', {}).get('usd', 0),
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices from CoinGecko: {e}")
        return None

def update_telegram_message():
    """Main function to update the Telegram message."""
    print("Starting bot...")
    bot = Bot(token=BOT_TOKEN)
    prices = get_crypto_prices()

    if prices:
        try:
            tehran_tz = pytz.timezone("Asia/Tehran")
            now = datetime.now(tehran_tz)
            update_time_str = now.strftime("%Y/%m/%d - %H:%M:%S")

            final_text = MESSAGE_TEMPLATE.format(
                btc=prices['btc'],
                eth=prices['eth'],
                sol=prices['sol'],
                bnb=prices['bnb'],
                xrp=prices['xrp'],
                doge=prices['doge'],
                ada=prices['ada'],
                trx=prices['trx'],
                shib=prices['shib'],
                ton=prices['ton'],
                update_time=update_time_str
            )

            bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=MESSAGE_ID,
                text=final_text,
                parse_mode=None
            )
            print(f"Message updated successfully at {update_time_str}")
        except TelegramError as e:
            print(f"Telegram API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Could not fetch prices. Update failed.")

if __name__ == "__main__":
    update_telegram_message()
