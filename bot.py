import os
import time
import random
import requests
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

def _norm_base(url: str) -> str:
    return url.rstrip("/")

TOKEN = (os.getenv("TOKEN") or "").strip()
BASE_URL = _norm_base(os.getenv("URL") or "https://api.telegram.org/bot")
ADMIN_ID = (os.getenv("ADMIN_ID") or "").strip()
API_URL = f"{BASE_URL}/bot{TOKEN}" if not BASE_URL.endswith("/bot") else f"{BASE_URL}{TOKEN}"

def handle_text(text: str) -> str:
    t = (text or "").strip().lower()
    if t in ("hi", "hello", "hey", "привет"):
        return "Салем! Черкани /help, чтобы увидеть, что я умею"
    if t == "csc31":
        return "Python"
    if t == "python":
        return "Версия 3.14 🐍"
    if t == "dice":
        _1 = random.randint(1, 6)
        _2 = random.randint(1, 6)
        return f"Ты выбросил {_1} и {_2}!\nИтого: {_1 + _2} 🎲"
    if t == "/help":
        return (
            "🛠 *Доступные команды:*\n\n"
            "/help — показать все команды\n"
            "/mood — узнать моё настроение \n"
            "/rest —  узнать как себя чувсвую \n"
            "/advice — получить совет от бота ️\n"
            "dice — бросить кости 🎲\n"
        )
    if t == "/mood":
        moods = [
            "Дайте чашечку кофе.",
            "Нормально. Перезагрузился, теперь снова живой.",
            "Хочу спать.",
            "В ударе! Как студент за 3 часа до дедлайна!",
            " Сплю, не мешай... ",
        ]
        return random.choice(moods)
    if t == "/rest":
        rests = [
            "Сегодня я не работаю, лень.",
            "‍Не хочу работать. Подожди до завтра.",
            " Ну сказал же, жди завтра :)",
        ]
        return random.choice(rests)
    if t == "/advice":
        advices = [
            "Не делай сегодня то, что можно отложить на после дедлайна",
            "Если я работаю - не спрашивай как я работаю. Я сам не знаю",
            "Сохраняй код,не забывай",
            "Не пиши комментарии в коде. Пусть тот кто читает,страдает",
            "Пей энергетики. Или кофе. Или оба сразу",
        ]
        return random.choice(advices)
    return "Сорян, не пониманте. черкани /help для списка команд."

def _get_updates(offset: Optional[int] = None, timeout: int = 25) -> Dict[str, Any]:
    assert API_URL, "TOKEN/URL не заданы (API_URL пуст)."
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    r = requests.get(f"{API_URL}/getUpdates", params=params, timeout=timeout + 5)
    r.raise_for_status()
    return r.json()

def _send_message(chat_id: int, text: str) -> None:
    assert API_URL, "TOKEN/URL не заданы (API_URL пуст)."
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{API_URL}/sendMessage", data=data, timeout=10)

def _extract_message(update: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    msg = update.get("message") or update.get("edited_message")
    if not isinstance(msg, dict):
        return None
    return msg

def main() -> None:
    if os.getenv("CI", "").lower() in ("1", "true", "yes"):
        print("CI mode detected — skipping long-poll loop.")
        return
    if not TOKEN or not BASE_URL:
        raise RuntimeError("Отсутствуют переменные окружения TOKEN/URL. Проверь .env и переменные в CircleCI.")
    next_offset: Optional[int] = None
    while True:
        try:
            data = _get_updates(offset=next_offset, timeout=25)
            ok = data.get("ok", False)
            result = data.get("result", [])
            if not ok or not isinstance(result, list):
                time.sleep(1)
                continue
            for upd in result:
                upd_id = upd.get("update_id")
                if isinstance(upd_id, int):
                    next_offset = upd_id + 1
                msg = _extract_message(upd)
                if not msg:
                    continue
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text")
                if chat_id is None:
                    continue
                reply = handle_text(text or "")
                _send_message(chat_id, reply)
        except requests.RequestException:
            time.sleep(2)
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    main()
