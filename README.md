# TRX Farming Bot

Minimal prototype of a Telegram bot with WebApp that simulates farming of TRX. It includes:
- Telegram bot using `aiogram` (`~=2.25`).
- Web application using `FastAPI` with an HTML/JS interface located in
  `templates/index.html`.
- Scheduler for automatic balance updates.
- Tron wallet generation via `tronpy`.

This project is for demonstration purposes.

## Running

Install dependencies and run both the bot and web app:

```bash
pip install -r requirements.txt
python bot.py &
uvicorn app:app --reload
```

The `requirements.txt` file pins `aiogram` to the `2.25` series so the bot
works with the expected API.

Set `WEBAPP_URL` in `.env` to the external URL where FastAPI is served so the bot
generates correct links.
