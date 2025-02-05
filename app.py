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


# 🔹 التحقق من وجود اسم العمود الصحيح
df.columns = df.columns.str.strip()  # إزالة أي مسافات زائدة

# البحث عن اسم العمود الصحيح
cartons_col = None
possible_names = ["Ctns", "Unnamed: 2"]  # الأسماء المحتملة للعمود

for col in df.columns:
    if col in possible_names:
        cartons_col = col
        break

# 🔹 تنظيف أسماء الأعمدة من أي مسافات زائدة
df.columns = df.columns.str.strip()

# 🔹 البحث عن العمود الصحيح لعدد الكراتين
cartons_col = None
possible_names = ["Ctns", "Unnamed: 2"]  # الأسماء المحتملة

for col in df.columns:
    if col in possible_names:
        cartons_col = col
        break

# 🔹 إذا تم العثور على العمود، نقوم بتنظيف البيانات وحذف الصفوف التي أقل من 10
if cartons_col:
    st.write(f"📌 تم التعرف على العمود: {cartons_col}")
    
    # عرض القيم في العمود قبل التحويل لمعرفة طبيعة البيانات
    st.write("🔍 القيم في العمود قبل التحويل:", df[cartons_col].unique())

    # تحويل القيم إلى أرقام، وإذا فشل التحويل تصبح القيم NaN
    df[cartons_col] = pd.to_numeric(df[cartons_col], errors="coerce")

    # عرض القيم بعد التحويل لمعرفة إذا تم التحويل بنجاح
    st.write("🔍 القيم في العمود بعد التحويل:", df[cartons_col].unique())

    # التأكد من وجود صفوف بعد الحذف
    rows_before = len(df)
    df = df[df[cartons_col].notna() & (df[cartons_col] >= 10)]
    rows_after = len(df)

    # إذا تم حذف أي صفوف، إظهار إشعار بذلك
    if rows_before > rows_after:
        st.success(f"✅ تم حذف {rows_before - rows_after} صفوف (عدد الكراتين أقل من 10).")
        save_data(df)  # حفظ التعديلات
    else:
        st.warning("⚠️ لم يتم حذف أي صفوف. تأكد من أن القيم في العمود صحيحة.")
else:
    st.warning("⚠️ لم يتم العثور على عمود 'Ctns' أو 'Unnamed: 2'. يرجى التحقق من ملف Excel.")

