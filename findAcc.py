from telethon.sync import TelegramClient

# Вставьте свои API_ID и API_HASH
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# Создаём клиент
with TelegramClient('session_name', api_id, api_hash) as client:
    username = 'example_username'  # Имя пользователя, которое вы хотите проверить
    try:
        # Получаем информацию о пользователе
        user = client.get_entity(username)
        print(f"Пользователь существует: {user.id}, имя: {user.first_name}")
    except ValueError:
        print("Пользователь с таким username не найден.")