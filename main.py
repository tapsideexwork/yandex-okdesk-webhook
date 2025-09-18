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
        # Получаем JSON с формы
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Нет JSON в запросе"}), 400

        print("Получен JSON от формы:", data, flush=True)  # логирование в Render

        # Тема заявки
        subject = "Заявка из Формы"

        # Формируем описание заявки (все данные формы)
        description = "Получены данные из Яндекс.Формы:\n\n"
        for key, value in data.items():
            description += f"{key}: {value}\n"

        # Payload для Okdesk
        payload = {
            "issue": {
                "subject": subject,
                "description": description,
                "client": {
                    "name": str(data.get("org_name", "Не указано")),
                    "inn": str(data.get("org_inn", "Не указано"))
                }
            }
        }

        headers = {
            "X-API-KEY": str(OKDESK_API_KEY),
            "Content-Type": "application/json"
        }

        # Отправка заявки в Okdesk
        response = requests.post(OKDESK_URL, json=payload, headers=headers)
        print("Ответ Okdesk:", response.text, flush=True)  # логируем полный ответ
        response.raise_for_status()  # выброс исключения при HTTP ошибке

        # Вернуть ID созданной заявки и статус
        okdesk_id = response.json().get("id")
        return jsonify({"status": "ok", "okdesk_id": okdesk_id})

    except requests.exceptions.HTTPError as http_err:
        print("HTTP ошибка при отправке в Okdesk:", http_err, flush=True)
        return jsonify({"status": "error", "message": str(http_err), "response": response.text}), 500
    except Exception as e:
        print("Ошибка при обработке webhook:", e, flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Render передаёт порт через переменную окружения
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
