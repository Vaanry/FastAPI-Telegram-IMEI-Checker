1. Клонируйте репозиторий:
    ```bash
    git clone git@github.com:Vaanry/FFastAPI-Telegram-IMEI-Checker.git
    cd FastAPI-Telegram-IMEI-Checker
    ```

2. Установите зависимости:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Настройте переменные окружения в `.env` файле.
    ```env
    APP_TITLE = Your store title
    DATABASE_URL = Your database url
    SECRET_KEY = Your secret key for jwt
    ALGORITHM = Your algorithm for jwt
    TOKEN = Your telegram token
    API_KEY = Токен API Live for IMEI checker service
    ```
4. Запустите миграции базы данных с помощью Alembic:

    ```bash
    alembic upgrade head
    ```
    
5. Запустите FastAPI-приложение:
    ```bash
    uvicorn app.main:app --reload
    ```
    
6. Откройте второе окно терминала, перейдите в директорию бота:
   ```bash
    cd bot
    ```
   
7. Запустите телеграм-бота:
   ```bash
    python bot.py
    ```

   
