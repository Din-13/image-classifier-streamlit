import streamlit as st
import requests
from PIL import Image
import io

API_URL = st.secrets.get("API_URL", "https://image-classifier-api-dinara.amvera.io")

st.title("Классификатор изображений")
st.write("Загрузите изображение, и нейронная сеть определит, что на нем изображено.")


uploaded_file = st.file_uploader("Выберите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)

    progress_text = "Классификация изображения..."
    progress_bar = st.progress(0)

    try:
        progress_bar.progress(25)
        st.text("Отправка изображения на сервер...")

        bytes_data = uploaded_file.getvalue()

        progress_bar.progress(50)

        files = {
            'file': (uploaded_file.name, bytes_data, f'image/{uploaded_file.name.split(".")[-1]}')
        }

        response = requests.post(
            f"{API_URL}/classify/",
            files=files
        )

        progress_bar.progress(75)

        if response.status_code == 200:
            result = response.json()
            predictions = result["predictions"]

            st.subheader("Результаты классификации:")

            table_data = {"№": [], "Класс": [], "Вероятность": []}

            for i, pred in enumerate(predictions):
                table_data["№"].append(i + 1)
                table_data["Класс"].append(pred['class_name'])
                table_data["Вероятность"].append(f"{pred['probability'] * 100:.2f}%")

            st.table(table_data)

            top_prediction = predictions[0]['class_name']
            st.success(f"Наиболее вероятный класс: **{top_prediction}**")

        else:
            st.error(f"Ошибка при обработке изображения: {response.text}")

        progress_bar.progress(100)

    except Exception as e:
        st.error(f"Произошла ошибка: {e}")