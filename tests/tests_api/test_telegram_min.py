import bot

# --- Minimal fake Response object ---
class _Resp:
    def __init__(self, payload=None, status_code=200):
        self._payload = payload or {}
        self.status_code = status_code
        self.text = str(self._payload)

    def json(self):
        return self._payload


# 1) Receive: last_update() returns the last update from Telegram
def test_receive_last_update_from_telegram(monkeypatch):
    payload = {
        "ok": True,
        "result": [
            {"update_id": 1, "message": {"chat": {"id": 111}, "text": "hi"}},
            {"update_id": 2, "message": {"chat": {"id": 222}, "text": "ping"}}],
    }
    called = {"url": None}

    def fake_get(url):
        called["url"] = url
        return _Resp(payload)

    monkeypatch.setattr(bot.requests, "get", fake_get)

    last = bot.last_update("https://api.telegram.org/botTOKEN/")
    assert last["update_id"] == 2
    assert called["url"].endswith("getUpdates")


# 2) Receive helpers: extract chat id and text from the same update
def test_receive_extracts_chat_id_and_text(monkeypatch):
    payload = {
        "ok": True,
        "result": [
            {"update_id": 5, "message": {"chat": {"id": 999}, "text": "  2 + 2  "}}],
    }

    def fake_get(url):
        return _Resp(payload)

    monkeypatch.setattr(bot.requests, "get", fake_get)

    upd = bot.last_update("https://api.telegram.org/botTOKEN/")
    assert bot.get_chat_id(upd) == 999
    assert bot.get_message_text(upd).strip() == "2 + 2"


# 3) Send: send_message() posts to sendMessage and returns 200
def test_send_message_to_telegram_ok(monkeypatch):
    called = {"url": None, "data": None}

    def fake_post(url, data=None, **kwargs):
        called["url"] = url
        called["data"] = data
        return _Resp({"ok": True}, status_code=200)

    monkeypatch.setattr(bot.requests, "post", fake_post)
    bot.url = "https://api.telegram.org/botTOKEN/"

    resp = bot.send_message(555, "Hello")
    assert resp.status_code == 200
    assert called["url"].endswith("sendMessage")


# 4) Send payload: chat_id and text are correct form fields
def test_send_message_payload_correct(monkeypatch):
    captured = {"data": None}

    def fake_post(url, data=None, **kwargs):
        captured["data"] = data
        return _Resp({"ok": True}, status_code=200)

    monkeypatch.setattr(bot.requests, "post", fake_post)
    bot.url = "https://api.telegram.org/botTOKEN/"

    bot.send_message(777, "Ping Pong")
    assert captured["data"] == {"chat_id": 777, "text": "Ping Pong"}