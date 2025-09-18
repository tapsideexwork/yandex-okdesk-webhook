from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# URL и API-ключ Okdesk
OKDESK_URL = "https://samoilenko.okdesk.ru/api/v1/issues?api_token=3a1d97301daf31b4e25a9dc37944fb3a1c56c0fd"
OKDESK_API_KEY = "3a1d97301daf31b4e25a9dc37944fb3a1c56c0fd"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print("Получен JSON от формы:", data, flush=True)

        # Заголовок заявки
        title = "Заявка из формы"

        # Формируем описание из всех данных формы
        description = "Получены данные из Яндекс.Формы:\n\n"
        for key, value in data.items():
            description += f"{key}: {value}\n"

        payload = {
            "issue": {
                "title": title,   # ✅ заменили subject -> title
                "description": description,
                "client": {
                    "name": data.get("org_name", "Не указано"),
                    "inn": data.get("org_inn", "Не указано")
                }
            }
        }

        headers = {
            "X-API-KEY": OKDESK_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(OKDESK_URL, json=payload, headers=headers)
        response.raise_for_status()

        return {"status": "ok", "okdesk_response": response.json()}

    except Exception as e:
        print("Ошибка при обработке webhook:", e, flush=True)
        return {"status": "error", "message": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)