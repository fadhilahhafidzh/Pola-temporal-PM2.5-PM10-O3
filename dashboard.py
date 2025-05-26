import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
import seaborn as sns

sns.set(style='dark')

st.set_page_config(page_title="Dashboard", page_icon="🔍")

# Load data
df = pd.read_csv('dashboard/main_data.csv', delimiter =",")

# Persiapan data untuk visualisasi
def get_pola_diurnal(df):
    pola_diurnal = df.groupby(['station', 'year', 'month', 'day', 'hour']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'O3': 'mean',
    }).reset_index()

    pola_diurnal.columns = ['station', 'year', 'month', 'day', 'hour', 'PM2.5', 'PM10', 'O3']
    pola_diurnal['date'] = pd.to_datetime(pola_diurnal[['year', 'month', 'day', 'hour']])
    
    return pola_diurnal

def get_pola_harian(df):
    pola_harian = df.groupby(['station', 'year', 'month', 'day']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'O3': 'mean',
    }).reset_index()

    pola_harian.columns = ['station', 'year', 'month', 'day', 'PM2.5', 'PM10', 'O3']
    pola_harian['BMUA_PM25'] = 75
    pola_harian['BMUA_PM10'] = 150
    pola_harian['BMUA_O3'] = 100

    return pola_harian

def get_bulanan(df):
    df_bulanan = df.groupby(['station', 'year', 'month']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'O3': 'mean',
    }).reset_index()

    df_bulanan.columns = ['station', 'year', 'month', 'PM2.5', 'PM10', 'O3']
    return df_bulanan

def get_clustering(df_bulanan):
    cat_PM25 = pd.cut(df_bulanan['PM2.5'], bins=3, labels=['Low', 'Medium', 'High'])
    cat_PM10 = pd.cut(df_bulanan['PM10'], bins=3, labels=['Low', 'Medium', 'High'])
    cat_O3 = pd.cut(df_bulanan['O3'], bins=3, labels=['Low', 'Medium', 'High'])

    table_PM25 = list(zip(df_bulanan['station'], df_bulanan['year'], df_bulanan['month'], df_bulanan['PM2.5'], cat_PM25))
    table_PM10 = list(zip(df_bulanan['station'], df_bulanan['year'], df_bulanan['month'], df_bulanan['PM10'], cat_PM10))
    table_O3 = list(zip(df_bulanan['station'], df_bulanan['year'], df_bulanan['month'], df_bulanan['O3'], cat_O3))

    df_table_PM25 = pd.DataFrame(table_PM25, columns=['Station','Tahun','Bulan', 'PM2.5', 'Kategori PM2.5'])
    df_table_PM10 = pd.DataFrame(table_PM10, columns=['Station','Tahun','Bulan', 'PM10', 'Kategori PM10'])
    df_table_O3 = pd.DataFrame(table_O3, columns=['Station','Tahun','Bulan', 'O3', 'Kategori O3'])

    cat_all = pd.concat([
        df_table_PM25.drop(columns=['PM2.5']),
        df_table_PM10.drop(columns=['Station', 'Tahun', 'Bulan', 'PM10']),
        df_table_O3.drop(columns=['Station', 'Tahun', 'Bulan', 'O3']),
    ], axis=1)

    cat_counts = cat_all.groupby(['Station', 'Tahun', 'Bulan'])[['Kategori PM2.5', 'Kategori PM10', 'Kategori O3']].apply(
        lambda x: x.apply(pd.Series.value_counts).fillna(0).astype(int)
    ).reset_index()

    df_melted = cat_counts.melt(id_vars=['Station','Tahun','level_3'], 
                              value_vars=['Kategori PM2.5', 'Kategori PM10', 'Kategori O3'],
                              var_name='Keterangan', value_name='value')

    #hanya mengambil kategori yang ada datanya (1)
    df_filtered = df_melted[df_melted['value'] == 1]

    #hitung bulan tiap kategori dan stasiun
    vis_cat = df_filtered.groupby(['Station', 'Tahun', 'level_3', 'Keterangan']).size().reset_index(name='Jumlah')
    vis_cat.columns = ['Station', 'Year', 'Kategori', 'Keterangan', 'Jumlah Bulan']
    return vis_cat

def get_vis_diurnal(pola_diurnal):
    return pola_diurnal.melt(
        id_vars=['station', 'year', 'month','day','hour','date'],
        value_vars=['PM2.5', 'PM10', 'O3'],
        var_name='Parameter', value_name='Nilai')

def get_vis_pm(pola_harian):
    vis_PM25 = pola_harian.melt(
        id_vars=['station', 'year', 'month', 'day'],
        value_vars=['PM2.5', 'BMUA_PM25'],
        var_name='Polutan', value_name='Konsentrasi (μg/m³)')
    vis_PM25['date'] = pd.to_datetime(vis_PM25[['year', 'month', 'day']])

    vis_PM10 = pola_harian.melt(
        id_vars=['station', 'year', 'month', 'day'],
        value_vars=['PM10', 'BMUA_PM10'],
        var_name='Polutan', value_name='Konsentrasi (μg/m³)')
    vis_PM10['date'] = pd.to_datetime(vis_PM10[['year', 'month', 'day']])

    vis_O3 = pola_harian.melt(
        id_vars=['station', 'year', 'month', 'day'],
        value_vars=['O3', 'BMUA_O3'],
        var_name='Polutan', value_name='Konsentrasi (μg/m³)')
    vis_O3['date'] = pd.to_datetime(vis_O3[['year', 'month', 'day']])

    return vis_PM25, vis_PM10, vis_O3

def get_vis_bulanan(bulanan_df):
    visualisasi_bulanan = bulanan_df.melt(
        id_vars=['station', 'year', 'month'],
        value_vars=['PM2.5', 'PM10', 'O3'],
        var_name='Parameter',
        value_name='Nilai'
    )
    visualisasi_bulanan['date'] = pd.to_datetime(
        visualisasi_bulanan[['year', 'month']].assign(day=1)
    )
    return visualisasi_bulanan


## Setup dashboard 
st.header("Dashboard: Polutan Udara Wilayah Urban, Suburban, dan Rural di Kota Beijing")
st.markdown(
    """
        <div style="text-align: justify;">
        <p>Keterangan</p>
        <ul>
            <li><b>Urban</b>: Station Wanshouxigong</li>
            <li><b>Suburban</b>: Station Changping</li>
            <li><b>Rural</b>: Station Huariou </li>
        </ul>
        </div>
    """
    , unsafe_allow_html=True
)

st.subheader("Pola Diurnal Polutan PM2.5, PM10, dan O₃")

# setup tanggal
min_date = df['date'].min()
max_date = df['date'].max()

with st.sidebar:
    st.header("Filter Tanggal")
    start_date, end_date = st.date_input(
        "Pilih rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

df['date'] = pd.to_datetime(df['date'])
main_df = df[(df['date'] >= pd.to_datetime(start_date)) & 
             (df['date'] <= pd.to_datetime(end_date))]


#df untuk kolom rata-rata
diurnal_df = get_pola_diurnal(main_df)
harian_df = get_pola_harian(main_df)
bulanan_df = get_bulanan(main_df)
clustering_df = get_clustering(bulanan_df)

#df untuk bantu visualisasi
vis_diurnal_df = get_vis_diurnal(diurnal_df)
vis_harian_PM25_df, vis_harian_PM10_df, vis_harian_O3_df = get_vis_pm(harian_df)
vis_bulanan_df = get_vis_bulanan(bulanan_df)
vis_cat = clustering_df.copy()


col1, col2, col3 = st.columns(3)

with col1:
    diurnal_pm25 = diurnal_df['PM2.5'].mean()
    st.metric(
        label="Rata-Rata PM2.5",
        value=f"{diurnal_pm25:.2f} μg/m³",
    )

with col2:
    diurnal_pm10 = diurnal_df['PM10'].mean()
    st.metric(
        label="Rata-Rata PM10",
        value=f"{diurnal_pm10:.2f} μg/m³",
    )

with col3:
    diurnal_o3 = diurnal_df['O3'].mean()
    st.metric(
        label="Rata-Rata O₃",
        value=f"{diurnal_o3:.2f} μg/m³",
    )


for parameter in vis_diurnal_df['Parameter'].unique():
    # Filter data untuk polutan tertentu
    df_polutan = vis_diurnal_df[vis_diurnal_df['Parameter'] == parameter]
    plt.figure(figsize=(8,5))
    sns.lineplot(
        data=df_polutan,
        x='hour', y='Nilai', hue='station'
    )
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):02d}:00"))
    plt.title(f"Rata-rata Diurnal {parameter}")
    plt.xlabel("Jam")
    plt.ylabel("Konsentrasi (μg/m³)")
    plt.legend(title='Station')
    plt.tight_layout()
    plt.show()

    st.pyplot(plt.gcf())
    plt.clf()  # Clear the figure for the next plot

st.subheader("Pola Harian Polutan PM2.5, PM10, dan O3")

col4, col5, col6 = st.columns(3)

with col4:
    harian_pm25 = harian_df['PM2.5'].mean()
    st.metric(
        label="Rata-Rata PM2.5",
        value=f"{harian_pm25:.2f} μg/m³",
    )

with col5:
    harian_pm10 = harian_df['PM10'].mean()
    st.metric(
        label="Rata-Rata PM10",
        value=f"{harian_pm10:.2f} μg/m³",
    )

with col6:
    harian_o3 = harian_df['O3'].mean()
    st.metric(
        label="Rata-Rata O₃",
        value=f"{harian_o3:.2f} μg/m³",
    )

# Visualisasi PM2.5
plt.figure(figsize=(15, 6))
line_PM25 = sns.lineplot(
    data=vis_harian_PM25_df,
    x='day', y='Konsentrasi (μg/m³)',
    hue='station', style='Polutan',
    style_order=['PM2.5', 'BMUA_PM25'],  # Tentukan urutan style
    dashes={'PM2.5': '', 'BMUA_PM25': (4, 2)},  # Solid untuk PM2.5, putus-putus untuk BMUA
    palette='hls'
)

line_PM25.set_title("Rata-rata Harian PM2.5", y=1.05)
line_PM25.set_xlabel("Hari")
line_PM25.set_ylabel("Konsentrasi (μg/m³)")
st.pyplot(plt.gcf())
plt.clf()  # Clear the figure for the next plot

# Visualisasi PM10
plt.figure(figsize=(15, 6))
line_PM10 = sns.lineplot(
    data=vis_harian_PM10_df,
    x='day', y='Konsentrasi (μg/m³)',
    hue='station', style='Polutan',
    style_order=['PM10', 'BMUA_PM10'],  # Tentukan urutan style
    dashes={'PM10': '', 'BMUA_PM10': (4, 2)},  # Solid untuk PM10, putus-putus untuk BMUA
    palette='hls'
)
line_PM10.set_title("Rata-rata Harian PM10", y=1.05)
line_PM10.set_xlabel("Hari")
line_PM10.set_ylabel("Konsentrasi (μg/m³)")
st.pyplot(plt.gcf())
plt.clf()  # Clear the figure for the next plot

#visualisasi harian O3
plt.figure(figsize=(15, 6))
line_PM10 = sns.lineplot(
    data=vis_harian_O3_df,
    x='day', y='Konsentrasi (μg/m³)',
    hue='station', style='Polutan',
    style_order=['O3', 'BMUA_O3'],
    dashes={'O3': '', 'BMUA_O3': (4, 2)},  # Solid untuk O3, putus-putus untuk BMUA
    palette='hls'
)

line_PM10.set_title("Rata-rata Harian O3", y=1.05)
line_PM10.set_xlabel("Hari")
line_PM10.set_ylabel("Konsentrasi (μg/m³)")
st.pyplot(plt.gcf())
plt.clf()  # Clear the figure for the next plot


st.subheader("Pola Bulanan Polutan PM2.5, PM10, dan O₃")

col7, col8, col9 = st.columns(3)

with col7:
    bulanan_pm25 = bulanan_df['PM2.5'].mean()
    st.metric(
        label="Rata-Rata PM2.5",
        value=f"{bulanan_pm25:.2f} μg/m³",
    )

with col8:
    bulanan_pm10 = bulanan_df['PM10'].mean()
    st.metric(
        label="Rata-Rata PM10",
        value=f"{bulanan_pm10:.2f} μg/m³",
    )

with col9:
    bulanan_o3 = bulanan_df['O3'].mean()
    st.metric(
        label="Rata-Rata O₃",
        value=f"{bulanan_o3:.2f} μg/m³",
    )

# Visualisasi Bulanan

# visualisasi pola bulanan rata-rata keseluruhan dalam bentuk barplot
for parameter in vis_bulanan_df['Parameter'].unique():
    df_polutan = vis_bulanan_df[
        (vis_bulanan_df['Parameter'] == parameter)]

    # Plot lineplot for this pollutant across all years
    plt.figure(figsize=(8,5))
    sns.barplot(
        data=df_polutan,
        x='month', y='Nilai', hue='station'
    )
    plt.title(f"Rata-rata Bulanan {parameter}") # Judul menunjukkan rata-rata keseluruhan
    plt.xlabel("Bulan")
    plt.ylabel("Konsentrasi (μg/m³)")
    plt.legend(title='Station')
    plt.tight_layout()
    plt.show()
    st.pyplot(plt.gcf())
    plt.clf()  # Clear the figure for the next plot

# visualisasi clustering-based binning
st.subheader("Analisis Lanjutan: Clustering-based Binning")
st.write("Disarankan untu memilih rentang tanggal yang lebih panjang untuk analisis ini.")

count_selected_months = pd.to_datetime(vis_bulanan_df['date']).dt.to_period('M').nunique()
col10 = st.columns(1)[0]
# Menampilkan jumlah bulan dalam analisis clustering
with col10:
    st.metric(
        label="Jumlah Bulan",
        value=f"{count_selected_months} bulan",
    )

#visualisasi data kategori
#visualisasi data kategori
for keterangan in vis_cat['Keterangan'].unique():
  plt.figure(figsize=(10,5))
  barplot_cat = sns.barplot(
      data=vis_cat[vis_cat['Keterangan'] == keterangan],
      x='Kategori', y='Jumlah Bulan', hue='Station', estimator = sum,
      palette='hls', errorbar= None,  order= ['High', 'Medium', 'Low']
  )
  plt.title(f"{keterangan}")
  plt.ylabel("Jumlah Bulan")
  plt.gca().yaxis.set_major_locator(MultipleLocator(1))
  plt.tight_layout()
  plt.show()

  st.pyplot(plt.gcf())
  plt.clf()  # Clear the figure for the next plot

