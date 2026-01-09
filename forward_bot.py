import telebot
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Bot Configuration
API_TOKEN = '8417577678:AAH6RXAvwsaEuhKSCq6AsC83tG5QBtd0aJk'

# Channel Configuration - O'zgartirishingiz mumkin
SOURCE_CHANNEL = '@TOSHKENTANGRENTAKSI'  # Manba kanal
DEST_CHANNEL = '@Angren_Toshkent_Taksi_pochta_a'  # Manzil kanal/guruh

bot = telebot.TeleBot(API_TOKEN)

# Channel post handler - kanaldan kelgan xabarlarni ushlaydi
@bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'animation', 'video_note', 'poll'])
def forward_channel_post(message):
    try:
        # Kanal ma'lumotlarini chiqarish
        channel_username = f"@{message.chat.username}" if message.chat.username else str(message.chat.id)
        print(f"📨 Xabar keldi: {message.chat.title} ({channel_username})")
        
        # Agar xabar manba kanaldan kelgan bo'lsa
        source_clean = SOURCE_CHANNEL.replace('@', '').lower()
        if message.chat.username and message.chat.username.lower() == source_clean:
            # Manzilga forward qilish
            bot.copy_message(
                chat_id=DEST_CHANNEL,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            print(f"✅ Forward qilindi: {DEST_CHANNEL}")
        else:
            print(f"⚠️  Bu manba kanal emas. Kutilgan: {SOURCE_CHANNEL}")
            
    except Exception as e:
        print(f"❌ Xatolik: {e}")

# Simple health check server for Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Forward Bot is running!')
    
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🌐 HTTP server: port {port}")
    server.serve_forever()

if __name__ == '__main__':
    print("="*50)
    print("🤖 FORWARD BOT ISHGA TUSHDI!")
    print(f"📥 Manba: {SOURCE_CHANNEL}")
    print(f"📤 Manzil: {DEST_CHANNEL}")
    print("="*50)
    
    # Start HTTP server for Render
    if os.environ.get('RENDER') or os.environ.get('PORT'):
        Thread(target=run_server, daemon=True).start()
    
    # Start bot
    print("⏳ Xabarlarni kutmoqda...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
