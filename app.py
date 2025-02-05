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


# 🔹 التحقق من وجود العمود وإصلاح أي مشاكل في الاسم
df.columns = df.columns.str.strip()  # إزالة أي مسافات زائدة
if "Ctns" in df.columns:
    st.write("📌 بيانات عمود Ctns قبل التحويل:", df["Ctns"].unique())  # عرض القيم لمعرفة طبيعتها
    
    df["Ctns"] = pd.to_numeric(df["Ctns"], errors="coerce")  # تحويل القيم إلى أرقام مع تجاهل الأخطاء
    df = df[df["Ctns"].notna() & (df["Ctns"] >= 10)]  # الاحتفاظ بالصفوف التي عدد الكراتين فيها 10 أو أكثر
    save_data(df)  # حفظ التعديلات تلقائيًا
    st.success("✅ تم حذف الصفوف التي تحتوي على أقل من 10 كراتين بنجاح!")
else:
    st.warning("⚠️ لم يتم العثور على عمود 'Ctns'، يرجى التحقق من اسم العمود في ملف Excel.")


