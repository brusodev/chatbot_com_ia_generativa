# link da API do CRUD
post_users = 'https://sdw-2023-prd.up.railway.app'
OPENIA_API_KEY = "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"

#!pip install openai

import pandas as pd
import requests
import json
import openai
from openai.api_resources import completion

openai.api_key = OPENIA_API_KEY


df = pd.read_csv('usuarios.csv')
users_ids = df['UserID'].tolist()
print(users_ids)

def get_user(id):
  response = requests.get(f'{post_users}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in users_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Você é um especialista em marketing bancário."},
      {"role": "user", "content": f"Crie uma mensagem para {user['name']} sobre a importancia dos investimentos (máximo de 100 caracteres)"}
    ]
  )
  
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.oi/santander-dev-week-2023-api/icon/credit.svg",
      "description": news
  })

def update_user(user):
  response = requests.put(f"{post_users}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")