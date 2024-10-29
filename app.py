import streamlit as st
import pandas as pd

# Τίτλος εφαρμογής
st.title('Διαχείριση Μεγάλου CSV Αρχείου')

# Προσθήκη του URL του αρχείου CSV από το Google Cloud
csv_url = "https://storage.googleapis.com/phonoograph_bucket/Database/New_DB_deleted_2mInactive_20240523%20(1).csv"

# Φόρτωση του CSV αρχείου από το URL
try:
    df = pd.read_csv(csv_url, dtype=str)  # Όλα τα δεδομένα ως string για αποφυγή σφαλμάτων τύπων
    st.write("Οι πρώτες 5 γραμμές του αρχείου:")
    st.write(df.head())
except Exception as e:
    st.write(f"Πρόβλημα με τη φόρτωση του αρχείου: {e}")

# Αναζήτηση σε συγκεκριμένη στήλη με πολλαπλούς όρους
if st.checkbox('Αναζήτηση σε δεδομένα'):
    search_column = st.selectbox('Επιλέξτε στήλη για αναζήτηση', df.columns)
    search_terms = st.text_input('Εισάγετε όρους αναζήτησης, διαχωρισμένους με κόμμα')
    
    if st.button('Αναζήτηση'):
        terms = [term.strip() for term in search_terms.split(',')]  # Διαχωρισμός και αφαίρεση κενών
        # Φιλτράρισμα για γραμμές που περιέχουν οποιονδήποτε από τους όρους
        results = df[df[search_column].apply(lambda x: any(term in str(x) for term in terms))]
        st.write(f"Βρέθηκαν {len(results)} αποτελέσματα.")
        st.write(results)

# Προσθήκη νέας σειράς
if st.checkbox('Προσθήκη νέας σειράς'):
    st.write("Προσθέστε μια νέα σειρά")
    new_data = {}
    for column in df.columns:
        new_data[column] = st.text_input(f"Νέα τιμή για τη στήλη {column}")
    
    if st.button('Προσθήκη'):
        # Προσθήκη της νέας σειράς στο DataFrame
        df = df.append(new_data, ignore_index=True)
        st.write("Η νέα σειρά προστέθηκε!")
        st.write(df.tail())  # Εμφάνιση των τελευταίων γραμμών για έλεγχο

# Διαγραφή σειράς με βάση το index
if st.checkbox('Διαγραφή σειράς'):
    delete_index = st.number_input('Εισάγετε τον αριθμό της σειράς για διαγραφή', min_value=0, max_value=len(df)-1)
    
    if st.button('Διαγραφή'):
        df = df.drop(delete_index).reset_index(drop=True)
        st.write(f"Η σειρά {delete_index} διαγράφηκε.")
        st.write(df)

# Κατεβάστε το επεξεργασμένο αρχείο CSV
if st.checkbox('Λήψη του επεξεργασμένου αρχείου CSV'):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Κατεβάστε το επεξεργασμένο CSV", data=csv, file_name='modified_data.csv', mime='text/csv')
