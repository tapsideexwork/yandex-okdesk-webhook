from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Адрес API Okdesk
OKDESK_URL = "https://samoilenko.okdesk.ru/api/v1/issues"
# Твой API-ключ Okdesk (замени на реальный)
OKDESK_API_KEY = "3a1d97301daf31b4e25a9dc37944fb3a1c56c0fd"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
    print("Получен JSON от формы:", data)  # временный вывод в логи

        # Заголовок заявки
        subject = "Заявка из Формы"

        # Собираем комментарий из всех полей формы
        description = "Получены данные из Яндекс.Формы:\n\n"
        for key, value in data.items():
            description += f"{key}: {value}\n"

        # Формируем payload для Okdesk
        payload = {
            "issue": {
                "subject": subject,
                "description": description,
                "client": {
                    "name": data.get("org_name", "Не указано"),
                    "inn": data.get("org_inn", "Не указано")
                }
            }
        }

        # Заголовки для Okdesk API
        headers = {
            "X-API-KEY": OKDESK_API_KEY,
            "Content-Type": "application/json"
