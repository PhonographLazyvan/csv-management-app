import streamlit as st
import pandas as pd

# Τίτλος εφαρμογής
st.title('Διαχείριση Μεγάλου CSV Αρχείου')

# Ανεβάστε ένα αρχείο CSV
uploaded_file = st.file_uploader("Ανεβάστε το αρχείο CSV", type="csv")

if uploaded_file is not None:
    # Φόρτωση του CSV αρχείου σε pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Εμφάνιση πρώτων 5 γραμμών για επιβεβαίωση
    st.write("Οι πρώτες 5 γραμμές του αρχείου:")
    st.write(df.head())
    
    # Αναζήτηση σε συγκεκριμένη στήλη
    search_column = st.selectbox('Επιλέξτε στήλη για αναζήτηση', df.columns)
    search_term = st.text_input('Εισάγετε όρο αναζήτησης')
    
    if st.button('Αναζήτηση'):
        results = df[df[search_column].str.contains(search_term, na=False)]
        st.write(f"Βρέθηκαν {len(results)} αποτελέσματα.")
        st.write(results)
    
    # Προσθήκη νέας σειράς (μέσω form)
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
    delete_index = st.number_input('Εισάγετε τον αριθμό της σειράς για διαγραφή', min_value=0, max_value=len(df)-1)
    
    if st.button('Διαγραφή'):
        df = df.drop(delete_index).reset_index(drop=True)
        st.write(f"Η σειρά {delete_index} διαγράφηκε.")
        st.write(df)

