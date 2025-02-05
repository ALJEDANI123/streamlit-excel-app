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

    # استرجاع الأعمدة المحذوفة مسبقًا
    if "cols_to_remove" in settings:
        df = df.drop(columns=settings["cols_to_remove"], errors="ignore")

    # استرجاع الصفوف المحذوفة مسبقًا
    if "rows_to_remove" in settings:
        df = df.drop(index=settings["rows_to_remove"], errors="ignore")

    # خيار لحذف الأعمدة
    cols_to_remove = st.multiselect("🗑️ اختر الأعمدة لحذفها", df.columns, default=settings.get("cols_to_remove", []))
    if cols_to_remove:
        df = df.drop(columns=cols_to_remove, errors="ignore")
        settings["cols_to_remove"] = cols_to_remove
        save_settings(settings)

    # عرض الجدول مع إمكانية حذف الصفوف يدويًا
    st.subheader("✏️ قم بحذف الصفوف مباشرة من الجدول:")
    edited_df = st.data_editor(df, num_rows="dynamic", key="table_editor")

    # تحديد الصفوف المحذوفة
    deleted_rows = list(set(df.index) - set(edited_df.index))
    if deleted_rows:
        settings["rows_to_remove"] = deleted_rows
        save_settings(settings)

    # زر لتحميل الملف بعد التعديلات
    st.download_button("📥 تحميل الملف بعد التعديل", edited_df.to_csv(index=False).encode("utf-8"), "modified_data.csv", "text/csv")
