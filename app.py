import streamlit as st
import pandas as pd
import pickle
import os

DATA_FILE = "saved_data.pkl"  # ملف لحفظ التعديلات

# وظيفة لحفظ البيانات في ملف pickle
def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

# وظيفة لتحميل البيانات من ملف pickle
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return None

st.title("📊 تعديل وعرض ملفات Excel")

# رفع ملف Excel
uploaded_file = st.file_uploader("📂 رفع ملف Excel", type=["xlsx", "xls"])

# تحميل البيانات المعدلة المحفوظة مسبقًا
saved_data = load_data()

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # إذا كانت هناك بيانات محفوظة، استخدمها بدلاً من البيانات الجديدة
    if saved_data is not None:
        df = saved_data

    # 🔹 خيار لحذف الأعمدة
    cols_to_remove = st.multiselect("🗑️ اختر الأعمدة لحذفها", df.columns)
    if cols_to_remove:
        df = df.drop(columns=cols_to_remove, errors="ignore")
        save_data(df)  # حفظ التعديلات

    # 🔹 عرض الجدول مع إمكانية حذف الصفوف يدويًا
    st.subheader("✏️ قم بحذف الصفوف مباشرة من الجدول:")
    edited_df = st.data_editor(df, num_rows="dynamic", key="table_editor")

    # تحديث البيانات المحفوظة بعد تعديل الجدول
    save_data(edited_df)

    # 🔹 زر لإعادة تحميل البيانات الأصلية من الملف
    if st.button("🔄 إعادة تعيين الجدول"):
        df = pd.read_excel(uploaded_file)  # استرجاع البيانات الأصلية
        save_data(df)  # تحديث البيانات المحفوظة

    # 🔹 زر لتحميل الملف بعد التعديلات
    st.download_button("📥 تحميل الملف بعد التعديل", edited_df.to_csv(index=False).encode("utf-8"), "modified_data.csv", "text/csv")




import os

ORIGINAL_DATA_FILE = "original_data.pkl"  # ملف لحفظ البيانات الأصلية

# 🔹 تحميل البيانات الأصلية فقط إذا كان الملف موجودًا
original_data = None
if os.path.exists(ORIGINAL_DATA_FILE):
    original_data = load_data(ORIGINAL_DATA_FILE)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 🔹 إذا لم يتم حفظ البيانات الأصلية مسبقًا، نقوم بحفظها
    if original_data is None:
        save_data(df, ORIGINAL_DATA_FILE)  # حفظ النسخة الأصلية
        original_data = df.copy()  # الاحتفاظ بنسخة محلية من البيانات الأصلية

    # 🔹 زر لاسترجاع البيانات الأصلية
    if st.button("🔄 استرجاع البيانات الأصلية"):
        df = original_data.copy()  # استرجاع النسخة الأصلية من البيانات
        save_data(df, DATA_FILE)  # تحديث الملف المعدل
        st.success("✅ تم استرجاع البيانات الأصلية!")




