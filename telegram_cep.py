import os
import requests

def format_product_message(product):
    title = product.get("title", "🛍️ Ürün adı bulunamadı")
    price = product.get("price", "Fiyat alınamadı")
    old_price = product.get("old_price", "")  # 👈 Yeni satır
    link = product.get("link", "#")
    discount = product.get("discount", "")
    rating = product.get("rating", "")
    colors = product.get("colors", [])
    specs = product.get("specs", [])

    if "TL" not in price:
        price = f"{price} TL"
    if old_price and "TL" not in old_price:
        old_price = f"{old_price} TL"

    indirimbilgi = f"%{discount}" if discount and discount.isdigit() else ""
    stars = f"⭐ {rating}" if rating else ""
    renkler = ", ".join([c["color"] for c in colors]) if colors else ""
    teknik = "\n".join([f"▫️ {spec}" for spec in specs]) if specs else ""

    if old_price and old_price != price:
        fiyat_bilgisi = (
            f"🔻 *Eski fiyat:* *{old_price}*\n"
            f"💰 *Yeni fiyat:* *{price}*"
        )
    else:
        fiyat_bilgisi = f"💰 *{price}*"

    return (
        f"*{title}*\n"
        f"{indirimbilgi}  {stars}\n"
        f"{teknik}\n"
        f"{f'🎨 Renkler: {renkler}' if renkler else ''}\n"
        f"{fiyat_bilgisi}\n"
        f"🔗 [🔥🔥 FIRSATA GİT 🔥🔥]({link})"
    )

def send_message(product):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    base_url = f"https://api.telegram.org/bot{token}"

    if not token or not chat_id:
        print("❌ BOT_TOKEN veya CHAT_ID tanımlı değil.")
        return

    message = format_product_message(product)
    image_url = product.get("image")

    try:
        if image_url and image_url.startswith("http"):
            payload = {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"{base_url}/sendPhoto", data=payload)
        else:
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"{base_url}/sendMessage", data=payload)

        if response.status_code == 200:
            print(f"✅ Gönderildi: {product.get('title', 'Ürün')}")
        else:
            print(f"❌ Gönderim hatası: {product.get('title', 'Ürün')} → {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")
