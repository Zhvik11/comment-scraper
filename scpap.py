import streamlit as st
import pandas as pd
import re
from collections import Counter
import random

st.set_page_config(page_title="Генератор миссий", layout="wide")

# Загружаем CSV
@st.cache_data
def load_data():
    return pd.read_csv("rope_hero_reviews.csv")

df = load_data()

st.title("Генератор миссий и анализ отзывов")
st.markdown("Отправь ссылку друзьям: просто разверни приложение на [Streamlit Cloud](https://share.streamlit.io) или в локальной сети.")

# --- Фильтр отзывов по ключевым словам ---
st.header("🔍 Поиск по ключевым словам")
search_term = st.text_input("Введите ключевое слово (например, 'миссия', 'босс'):")

if search_term:
    filtered = df[df['content'].str.contains(search_term, case=False, na=False)]
    st.write(f"Найдено {len(filtered)} отзывов:")
    st.dataframe(filtered[['content']].head(20))

# --- Генератор идей миссий ---
st.header("Генератор идей миссий из отзывов")

mission_phrases = [
    r'добавьте.*?\.', r'сделайте.*?\.', r'предлагаю.*?\.',
    r'я бы хотел.*?\.', r'мне бы хотелось.*?\.', r'хочу миссию.*?\.'
]

suggestions = []
for text in df['content'].dropna():
    for pattern in mission_phrases:
        found = re.findall(pattern, text.lower())
        suggestions.extend(found)

unique_missions = list(set(s.strip().capitalize() for s in suggestions if len(s.strip()) > 10))

if unique_missions:
    st.success(f"Найдено {len(unique_missions)} потенциальных миссий")
    st.write(random.sample(unique_missions, min(10, len(unique_missions))))
else:
    st.warning("Нет подходящих фраз для генерации.")

# --- Простая генерация миссий по команде ---
st.header("🎮 Генерация миссии по команде")
user_command = st.text_input("Введите команду: (например, 'сделай миссию с боссом' или 'миссия с машиной')")

# Словарь ключевых слов и примеров генерации
mission_keywords = {
    'босс': ["Сразиться с гигантским боссом в центре города", "Победить мутанта с суперспособностями на арене"],
    'враг': ["Уничтожить волну врагов на складе", "Защитить базу от нападения преступников"],
    'машина': ["Угнать бронированный грузовик под охраной", "Устроить гонку по улицам города"],
    'щупальца': ["Использовать щупальца, чтобы захватить вражеский вертолет", "Сломать защиту базы с помощью суперщупалец"]
}

generated = []
if user_command:
    for key, ideas in mission_keywords.items():
        if key in user_command.lower():
            generated.extend(ideas)

if generated:
    st.subheader(" Сгенерированные идеи миссий:")
    st.write(random.choice(generated))
else:
    if user_command:
        st.info("Ключевых слов в команде не найдено. Попробуй использовать: босс, враг, машина, щупальца")





