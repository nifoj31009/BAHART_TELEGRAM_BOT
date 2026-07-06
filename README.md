# BAHART_TELEGRAM_BOT

This branch adds a minimal Python scaffold so you can run a Socket.IO client and
forward incoming events to Telegram for testing.

Quickstart
----------
1. Clone and checkout the branch:

   git clone https://github.com/nifoj31009/BAHART_TELEGRAM_BOT.git
   cd BAHART_TELEGRAM_BOT
   git checkout scaffold/mvp

2. Copy the example env and fill your values:

   copy .env.example .env   # on Windows (PowerShell: cp .env.example .env)
   # Edit .env and set DATA_WS_URL, WS_AUTH_TOKEN (if needed), TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

3. Create a virtualenv and install dependencies:

   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

4. Run the verbose tester to see raw incoming WS events:

   python app/ws_verbose.py

5. When the WS connection works, run the main service which will forward events to Telegram:

   python app/main.py

Docker
------
Build and run with Docker (optional):

   docker build -t bahart-tele-bot .
   docker run --env-file .env bahart-tele-bot

Notes
-----
- Do NOT commit real secrets to the repository. Use .env (which should be in .gitignore).
- If the WS server requires an Origin header or a cookie for authentication, set WS_ORIGIN
  and WS_COOKIE in your .env with the appropriate values.
