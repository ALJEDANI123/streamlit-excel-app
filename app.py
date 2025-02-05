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

st.title("📊 عرض وتحرير ملفات Excel")

# رفع ملف Excel
uploaded_file = st.file_uploader("📂 رفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    settings["last_file"] = uploaded_file.name
    save_settings(settings)

    st.subheader("🔍 البيانات الأصلية")
    st.dataframe(df)

    # 🔹 حذف الأعمدة المختارة مسبقًا
    cols_to_remove = st.multiselect("🗑️ اختر الأعمدة لحذفها", df.columns, default=settings.get("cols_to_remove", []))
    if cols_to_remove:
        df = df.drop(columns=cols_to_remove, errors="ignore")
        settings["cols_to_remove"] = cols_to_remove
        save_settings(settings)

    # 🔹 حذف الصفوف التي لا تحتوي على أرقام في عمود معين
    selected_col_for_numbers = st.selectbox("🔢 اختر عمود للتحقق من وجود أرقام", df.columns, index=0)
    if selected_col_for_numbers:
        df = df[df[selected_col_for_numbers].astype(str).str.isnumeric()]
        settings["selected_col_for_numbers"] = selected_col_for_numbers
        save_settings(settings)

    # 🔹 حذف الصفوف التي يكون فيها عدد الكراتين أقل من 10
    cartons_col = st.selectbox("📦 اختر عمود عدد الكراتين", df.columns, index=0)
    if cartons_col:
        df[cartons_col] = pd.to_numeric(df[cartons_col], errors="coerce")  # تحويل القيم إلى أرقام
        df = df[df[cartons_col] >= 10]
        settings["cartons_col"] = cartons_col
        save_settings(settings)

    # 🔹 إضافة عمود جديد
    new_col_name = st.text_input("➕ اسم العمود الجديد", value=settings.get("new_col_name", ""))
    new_col_values = st.text_area("📝 قيم العمود الجديد (افصل القيم بأسطر جديدة)", value=settings.get("new_col_values", ""))
    
    if new_col_name and new_col_values:
        new_values_list = new_col_values.split("\n")
        if len(new_values_list) == len(df):
            df[new_col_name] = new_values_list
            settings["new_col_name"] = new_col_name
            settings["new_col_values"] = new_col_values
            save_settings(settings)
        else:
            st.warning("⚠️ عدد القيم لا يتطابق مع عدد الصفوف!")

    # 🔹 عرض البيانات بعد التعديل
    st.subheader("✅ البيانات بعد التعديلات")
    st.dataframe(df)

    # 🔹 تنزيل الملف المعدل
    st.download_button("📥 تحميل الملف بعد التعديل", df.to_csv(index=False).encode("utf-8"), "modified_data.csv", "text/csv")
