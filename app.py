import streamlit as st
import pandas as pd

# تحميل ملف Excel
st.title("عرض وتحرير ملفات Excel")

uploaded_file = st.file_uploader("رفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file:
    # قراءة ملف Excel
    df = pd.read_excel(uploaded_file)

    # عرض البيانات الأصلية
    st.subheader("البيانات الأصلية")
    st.dataframe(df)

    # تحديد الأعمدة والصفوف المراد حذفها
    cols_to_remove = st.multiselect("اختر الأعمدة لحذفها", df.columns)
    rows_to_remove = st.multiselect("اختر الصفوف لحذفها (حسب الفهرس)", df.index.tolist())

    # تعديل البيانات
    if cols_to_remove:
        df = df.drop(columns=cols_to_remove)
    if rows_to_remove:
        df = df.drop(index=rows_to_remove)

    # إضافة عمود جديد
    new_col_name = st.text_input("اسم العمود الجديد")
    new_col_values = st.text_area("قيم العمود الجديد (افصل القيم بأسطر جديدة)")

    if new_col_name and new_col_values:
        new_values_list = new_col_values.split("\n")
        if len(new_values_list) == len(df):
            df[new_col_name] = new_values_list
        else:
            st.warning("عدد القيم لا يتطابق مع عدد الصفوف!")

    # عرض البيانات المعدلة
    st.subheader("البيانات بعد التعديل")
    st.dataframe(df)

    # تنزيل الملف المعدل
    st.download_button("تحميل الملف بعد التعديل", df.to_csv(index=False).encode("utf-8"), "modified_data.csv", "text/csv")

