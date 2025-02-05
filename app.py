import streamlit as st
import pandas as pd
import json

SETTINGS_FILE = "settings.json"

# وظيفة لحفظ الإعدادات
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

# وظيفة لتحميل الإعدادات
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# تحميل الإعدادات المحفوظة
settings = load_settings()

st.title("📊 تعديل وعرض ملفات Excel")

# رفع ملف Excel
uploaded_file = st.file_uploader("📂 رفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # استرجاع الأعمدة المحذوفة سابقًا
    if "cols_to_remove" in settings:
        df = df.drop(columns=settings["cols_to_remove"], errors="ignore")

    # استرجاع الصفوف المحذوفة سابقًا
    if "rows_to_remove" in settings:
        df = df.drop(index=settings["rows_to_remove"], errors="ignore")

    st.subheader("✏️ قم بالتعديل مباشرة على الجدول:")
    edited_df = st.data_editor(df, num_rows="dynamic", key="table_editor")

    # تحديث الإعدادات عند التعديل
    settings["cols_to_remove"] = list(set(df.columns) - set(edited_df.columns))  # الأعمدة المحذوفة
    settings["rows_to_remove"] = list(set(df.index) - set(edited_df.index))  # الصفوف المحذوفة

    # حفظ الإعدادات
    save_settings(settings)

    # زر لتنزيل الملف المعدل
    st.download_button("📥 تحميل الملف بعد التعديل", edited_df.to_csv(index=False).encode("utf-8"), "modified_data.csv", "text/csv")
