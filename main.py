from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ����� API Okdesk
OKDESK_URL = "https://samoilenko.okdesk.ru/api/v1/issues"
# ���� API-���� Okdesk (������ �� ��������)
OKDESK_API_KEY = "3a1d97301daf31b4e25a9dc37944fb3a1c56c0fd"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json

        # ��������� ������
        subject = "������ �� �����"

        # �������� ����������� �� ���� ����� �����
        description = "�������� ������ �� ������.�����:\n\n"
        for key, value in data.items():
            description += f"{key}: {value}\n"

        # ��������� payload ��� Okdesk
        payload = {
            "issue": {
                "subject": subject,
                "description": description,
                "client": {
                    "name": data.get("org_name", "�� �������"),
                    "inn": data.get("org_inn", "�� �������")
                }
            }
        }

        # ��������� ��� Okdesk API
        headers = {
            "X-API-KEY": OKDESK_API_KEY,
            "Content-Type": "application/json"
