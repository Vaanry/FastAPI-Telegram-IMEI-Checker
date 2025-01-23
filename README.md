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

4. Запустите FastAPI-приложение:
    ```bash
    uvicorn app.main:app --reload
    ```
5. Откройте второе окно терминала, перейдите в директорию бота:
   ```bash
    cd bot
    ```
6. Запустите телеграм-бота:
   ```bash
    python bot.py
    ```

   
