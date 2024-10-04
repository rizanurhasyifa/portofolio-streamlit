import streamlit as st
import pandas as pd
import plotly.express as px

# Judul aplikasi
st.title('Visualisasi Outcome Austin Animal Center Menggunakan Plotly')

# Membaca dataset langsung dari folder
csv_file_path = 'Austin_Animal_Center_Outcomes.csv'  # Ganti dengan nama file CSV yang sesuai
df = pd.read_csv(csv_file_path)

# Mengubah datatype DateTime
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])

# Drop kolom tidak penting
df = df.drop(columns=['Animal ID'])

# Membuat kolom baru yang berisi hanya tahun outcome, bulan, dan hari
df['year_outcome'] = df['DateTime'].dt.year
df['month_outcome'] = df['DateTime'].dt.month
df['day_outcome'] = df['DateTime'].dt.day

# Membuat kolom baru yang berisi hanya tahun lahir, bulan, dan hari
df['year_lahir'] = df['Date of Birth'].dt.year
df['month_lahir'] = df['Date of Birth'].dt.month
df['day_lahir'] = df['Date of Birth'].dt.day

# Menghitung umur dalam bulan
days = (df['DateTime'] - df['Date of Birth']).dt.days
average_days_per_month = 30.44
df['age_upon_outcome_months'] = days / average_days_per_month

# Drop kolom Outcome Subtype
df = df.drop(columns=['Outcome Subtype'])

# Handle missing values
df['Name'] = df['Name'].fillna('No Name')
df['Name'] = df['Name'].apply(lambda x: 'Has Name' if x != 'No Name' else 'No Name')
df['Outcome Type'].fillna(df['Outcome Type'].mode()[0], inplace=True)
df['Sex upon Outcome'].fillna(df['Sex upon Outcome'].mode()[0], inplace=True)
df['Age upon Outcome'].fillna(df['Age upon Outcome'].mode()[0], inplace=True)

df = df.drop_duplicates()

# Select box untuk memilih visualisasi
visualization_option = st.selectbox(
    'Pilih visualisasi yang ingin ditampilkan:',
    ['Distribusi Umur Hewan', 'Distribusi Tipe Hewan', 'Distribusi Outcome Type']
)

# Menampilkan visualisasi sesuai pilihan
if visualization_option == 'Distribusi Umur Hewan':
    st.subheader("Distribusi Umur Hewan dalam Bulan")
    
    # Filter untuk umur >= 0
    valid_age_df = df[df['age_upon_outcome_months'] >= 0]

    fig_age_months = px.histogram(valid_age_df, x='age_upon_outcome_months', nbins=20, title='Distribusi Umur Hewan dalam Bulan')
    st.plotly_chart(fig_age_months)

elif visualization_option == 'Distribusi Tipe Hewan':
    st.subheader("Distribusi Tipe Hewan (Animal Type)")
    animal_type_counts = df['Animal Type'].value_counts()
    fig_animal_type = px.pie(
        names=animal_type_counts.index,
        values=animal_type_counts.values,
        title='Distribusi Tipe Hewan',
        hole=0.3,  # Untuk membuat donut chart
        width=800,  # Menentukan lebar chart
        height=600  # Menentukan tinggi chart
    )
    st.plotly_chart(fig_animal_type)

elif visualization_option == 'Distribusi Outcome Type':
    st.subheader("Distribusi Outcome Type")
    fig_outcome_type = px.histogram(df, x='Outcome Type', title='Distribusi Outcome Type', color='Outcome Type', text_auto=True)
    st.plotly_chart(fig_outcome_type)
