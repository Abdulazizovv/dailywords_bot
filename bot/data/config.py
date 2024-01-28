from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# CHANNEL_ID = 1376269802
CHANNEL_ID = -1001918354190
# IP = env.str("ip")  # Xosting ip manzili
# password = env.str("PASSWORD")  # Xosting ip manzili

