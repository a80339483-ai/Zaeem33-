import asyncio
import os
import pandas_ta as ta
from telegram import Bot
import yfinance as yf

# قراءة البيانات الآمنة
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "@zaeem33")

PAIRS = {
    "EURUSD=X": "EUR/USD",
    "GBPUSD=X": "GBP/USD",
    "USDJPY=X": "USD/JPY",
    "AUDUSD=X": "AUD/USD",
    "GC=F": "الذهب (GOLD)",
}


async def start_signals_engine():
    bot = Bot(token=TELEGRAM_TOKEN)
    print("🚀 تم تشغيل بوت 'زعيم التداول' على السحابة بنجاح!")

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="⚡ **تم تشغيل محرك التوصيات الدائم (24/7) لـ 'زعيم التداول' بنجاح!**",
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"خطأ في إرسال رسالة الترحب: {e}")

    while True:
        for symbol, name in PAIRS.items():
            try:
                df = yf.download(
                    tickers=symbol, period="1d", interval="1m", progress=False
                )

                if not df.empty and len(df) >= 20:
                    df["RSI"] = ta.rsi(df["Close"], length=14)
                    last_rsi = round(df["RSI"].iloc[-1], 2)
                    last_price = round(df["Close"].iloc[-1], 5)

                    if last_rsi <= 30:
                        msg = f"""
🚨 **إشارة تداول جديدة - زعيم التداول** 🚨

📊 **الزوج:** {name}
📈 **الاتجاه:** 🟢 شراء (CALL)
⏱️ **مدة الصفقة:** 1 إلى 3 دقائق
🎯 **سعر الدخول:** {last_price}
📊 **مؤشر RSI:** {last_rsi} (تشبع بيعي)

⚠️ *تنبيه: التزم بإدارة رأس المال (1% - 2% فقط).*
"""
                        await bot.send_message(
                            chat_id=CHAT_ID, text=msg, parse_mode="Markdown"
                        )
                        print(f"✅ تم إرسال توصية شراء لـ {name}")
                        await asyncio.sleep(120)

                    elif last_rsi >= 70:
                        msg = f"""
🚨 **إشارة تداول جديدة - زعيم التداول** 🚨

📊 **الزوج:** {name}
📉 **الاتجاه:** 🔴 بيع (PUT)
⏱️ **مدة الصفقة:** 1 إلى 3 دقائق
🎯 **سعر الدخول:** {last_price}
📊 **مؤشر RSI:** {last_rsi} (تشبع شرائي)

⚠️ *تنبيه: التزم بإدارة رأس المال (1% - 2% فقط).*
"""
                        await bot.send_message(
                            chat_id=CHAT_ID, text=msg, parse_mode="Markdown"
                        )
                        print(f"✅ تم إرسال توصية بيع لـ {name}")
                        await asyncio.sleep(120)

            except Exception as e:
                print(f"خطأ أثناء فحص {name}: {e}")

        await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(start_signals_engine())
  
