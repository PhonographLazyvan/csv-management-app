import streamlit as st
import pandas as pd

# Τίτλος της εφαρμογής
st.title("CSV File Management App")

# Εισαγωγή του αρχείου CSV από το Google Cloud Storage
csv_url = "https://storage.googleapis.com/phonoograph_bucket/Database/New_DB_deleted_2mInactive_20240523%20(1).csv"

# Εμφάνιση μηνύματος κατά τη φόρτωση του αρχείου
st.write("Φόρτωση αρχείου CSV...")

# Ανάγνωση του CSV αρχείου με την παράμετρο low_memory=False για αποφυγή σφαλμάτων ανάμειξης τύπων δεδομένων
try:
    df = pd.read_csv(csv_url, low_memory=False)

    # Μετατροπή όλων των στηλών σε μορφή κειμένου (string)
    df = df.astype(str)

    # Εμφάνιση του DataFrame
    st.write("Επιτυχημένη φόρτωση του αρχείου CSV:")
    st.dataframe(df)

    # Προσθήκη δυνατότητας λήψης του επεξεργασμένου αρχείου CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Λήψη CSV αρχείου", data=csv, file_name='processed_file.csv', mime='text/csv')

    # Εμφάνιση βασικών στατιστικών για τους αριθμητικούς τύπους δεδομένων
    st.subheader("Στατιστικά δεδομένων")
    st.write(df.describe())

    # Προσθήκη δυνατότητας φιλτραρίσματος δεδομένων
    st.subheader("Φιλτράρισμα δεδομένων")
    column_to_filter = st.selectbox("Επίλεξε στήλη για φιλτράρισμα", df.columns)
    filter_value = st.text_input(f"Φίλτρο για την στήλη {column_to_filter}")

    if filter_value:
        filtered_df = df[df[column_to_filter].str.contains(filter_value, na=False)]
        st.write(f"Αποτελέσματα φιλτραρίσματος για '{filter_value}' στη στήλη '{column_to_filter}':")
        st.dataframe(filtered_df)

    # Προσθήκη δυνατότητας λήψης του φιλτραρισμένου αρχείου CSV
    if not filtered_df.empty:
        filtered_csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="Λήψη φιλτραρισμένου CSV αρχείου", data=filtered_csv, file_name='filtered_file.csv', mime='text/csv')

except Exception as e:
    st.error(f"Σφάλμα κατά τη φόρτωση του αρχείου CSV: {e}")
