import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
import os

st.set_page_config(page_title="Dashboard", page_icon="🔍")

st.image("https://i.pinimg.com/736x/93/8f/6a/938f6a4214868cde45f3de12a318adfb.jpg")
#ambil data dari csv
path = os.chdir("D:/Coba2 dicoding")
# Load data
visualisasi_bulanan = pd.read_csv("submission1/visualisasi_bulanan.csv", delimiter =",")
visualisasi_diurnal = pd.read_csv("submission1/visualisasi_diurnal.csv", delimiter =",")
vis_PM25 = pd.read_csv("submission1/PM25_harian.csv", delimiter =",")
vis_PM10 = pd.read_csv("submission1/PM10_harian.csv", delimiter =",")
vis_cat = pd.read_csv("submission1/vis_cat.csv", delimiter =",")
st.title("Proyek Analisis Data: Kualitas Udara Wilayah Urban, Suburban, dan Rural di Kota Beijing")
st.markdown(
    """
        <div style="text-align: justify;">
            Kualitas udara merupakan indikator penting dalam menilai tingkat kesehatan dan kesejahteraan, 
            khususnya di wilayah perkotaan dengan aktivitas manusia yang padat, salah satunya Kota Beijing. 
            Ibu kota Tiongkok ini berperan sebagai pusat ekonomi, sosial, serta politik yang menjadikan wilayah 
            ini lebih krusial dalam menghadapi tantangan industri, transportasi, dan urbanisasi yang masif. 
            Di sisi lain, wilayah suburban dan rural di sekitar Beijing memiliki karakteristik penggunaan lahan 
            dan sumber polusi yang berbeda, yang berdampak pada variasi tingkat kualitas udara. Alisis data ini dilakukan 
            dengan cara eksplorasi dan perbandingan pola temporal polutan PM2.5, PM10, dan O3 di antara tiga zona wilayah: 
            urban (Wanshouxigong), suburban (Changping), dan rural (Huariou) di Kota Beijing.
        </div>
    """
        , unsafe_allow_html=True)

st.markdown("---")
st.header("Pertanyaan Penelitian")
st.markdown(
    """
        <div style="text-align: justify;"> 
            1. Bagaimana pola bulanan polutan PM2.5, PM 10, dan O3 di wilayah urban (Wanshouxigong), suburban (Changping), dan rural (Huariou)?
            <br>
            2. Bagaimana pola diurnal polutan PM2.5, PM10, dan O3 di wilayah urban (Wanshouxigong), suburban (Changping), dan rural (Huariou)?
            <br>
            3. Apakah konsentrasi polutan PM2.5 dan PM10 di atas BMUA harian (24 jam) untuk wilayah urban (Wanshouxigong), suburban (Changping), dan rural (Huariou)?
            <br>
            4.Bagaimana kategori data rata-rata bulanan di wilayah urban (Wanshouxigong), suburban (Changping), dan rural (Huariou)?
        </div>
    """
        , unsafe_allow_html=True)

Tab1, Tab2, Tab3, Tab4 = st.tabs(["Pola Bulanan", "Pola Diurnal", "Pola Harian & BMUA", "Analisis Lanjutan"])
with Tab1:
    #menampilkan header
    st.header("Pola Bulanan")
    #tampilkan dataframe
    st.write("Data Rata-Rata Bulanan PM2.5, PM10, dan O₃")
    st.dataframe(visualisasi_bulanan)
    #nama subheader
    #visualisasi pola bulanan
    for polutan in visualisasi_bulanan['Polutan'].unique():
        # Filter data untuk polutan tertentu
        df_polutan = visualisasi_bulanan[visualisasi_bulanan['Polutan'] == polutan]
        # Plot lineplot untuk polutan ini
        plt.figure(figsize=(8,5))
        sns.lineplot(
            data=df_polutan,
            x='month', y='Konsentrasi', hue='station'
        )
        plt.title(f"Rata-rata Bulanan {polutan}")
        plt.xlabel("Bulan")
        plt.ylabel("Konsentrasi (μg/m³)")
        plt.legend(title='Station')
        plt.tight_layout()
        st.pyplot(fig=plt.gcf())
        plt.clf()

    st.markdown(
        """
            <div style="text-align: justify;">
                Pola bulanan PM2.5 dan PM10 menunjukkan dua puncak konsentrasi, yaitu pada awal tahun (Mei) dan akhir tahun (Desember) 
                dengan nilai terendah terjadi di pertengahan tahun (Agustus). Pola ini dipengaruhi sudut deklinasi matahari dan musiman. 
                Sebaliknya, konsentrasi O₃ mencapai puncaknya saat PM menurun, mengikuti pola yang berlawanan. Ozon troposfer semakin banyak 
                pada musim kering (Juni-Juli-Agustus) akibat meningkatnya radiasi matahari dan suhu yang mempercepat reaksi fotokimia antara 
                nitrogen oksida (NOₓ) dan senyawa organik volatil (VOC), sehingga menghasilkan O₃ dalam jumlah lebih tinggi.
            </div>
        """
        , unsafe_allow_html=True)


with Tab2:
    #menampilkan header
    st.header("Pola Diurnal")
    #tampilkan dataframe
    st.write("Data Rata-Rata Diurnal PM2.5, PM10, dan O₃")
    st.dataframe(visualisasi_diurnal)
    #nama subheader
    st.subheader("Pola Diurnal PM2.5, PM10, dan O₃")
    #barplot diurnal
    for polutan in visualisasi_diurnal['Polutan'].unique():
        # Filter data untuk polutan tertentu
        df_polutan = visualisasi_diurnal[visualisasi_diurnal['Polutan'] == polutan]
    
        # Plot lineplot untuk polutan ini
        plt.figure(figsize=(8,5))
        sns.lineplot(
            data=df_polutan,
            x='hour', y='Konsentrasi', hue='station'
        )
        plt.title(f"Rata-rata Diurnal {polutan}")
        plt.xlabel("Jam")
        plt.ylabel("Konsentrasi (μg/m³)")
        plt.legend(title='Station')
        plt.tight_layout()
        st.pyplot(fig=plt.gcf())
        plt.clf()
    #Pembahasan
    st.markdown(
        """
            <div style="text-align: justify;">
                Pola diurnal PM2.5 dan PM10 menunjukkan dua puncak konsentrasi, yaitu pukul 10.00 dan 19.00 dengan pola cenderung konstan. 
                Pola yang konstan menandakan kecenderungan aktivitas penghasil polusi yang sama disetiap waktu. Sementara itu, konsentrasi 
                O₃ hanya memiliki satu puncak pada pukul 16.00.
                Pola ini menunjukkan bahwa konsentrasi O₃ meningkat seiring dengan meningkatnya suhu dan radiasi matahari dengan <i>lag time</i> 
                sekitar 4 jam dari waktu puncak radiasi matahari pada umumnya.
            </div>
        """
        , unsafe_allow_html=True)
    

with Tab3:
    #membuat judul plot
    st.markdown(
        """
            <div style="text-align: justify;">
                <b>PM2.5</b> BMUA 24 jam = 75 μg/m³
                <br>
                <b>PM10</b> BMUA 24 jam = 150 μg/m³
            </div>
        """
        , unsafe_allow_html=True)
    #nama subheader
    st.subheader("Kualitas Udara Harian PM2.5")
    #tampilkan dataframe
    st.write("Data Rata-Rata PM2.5 Harian")
    st.dataframe(vis_PM25)
    #plot PM2.5
    #plot line harian PM10
    plt.figure(figsize=(15, 6))
    line_PM25 = sns.lineplot(
        data=vis_PM25,
        x='day', y='Konsentrasi (μg/m³)',
        hue='station', style='Polutan',
        style_order=['PM2.5', 'BMUA_PM25'],  # Tentukan urutan style
        dashes={'PM2.5': '', 'BMUA_PM25': (4, 2)},  # Solid untuk PM2.5, putus-putus untuk BMUA
        palette='Blues'
        )
    #judul plot
    line_PM25.set_title("Rata-rata Harian PM2.5", y=1.05)
    #nama sumbu x
    line_PM25.set_xlabel("Hari")
    #nama sumbu y
    line_PM25.set_ylabel("Konsentrasi (μg/m³)")
    st.pyplot(line_PM25.figure)

    #nama subheader
    st.subheader("Kualitas Udara Harian PM10")
    #tampilkan dataframe
    st.write("Data Rata-Rata PM10 Harian")
    st.dataframe(vis_PM10)
    #plot line harian PM10
    plt.figure(figsize=(15, 6))
    line_PM10 = sns.lineplot(
        data=vis_PM10,
        x='day', y='Konsentrasi (μg/m³)',
        hue='station', style='Polutan',
        style_order=['PM10', 'BMUA_PM10'],
        dashes={'PM10': '', 'BMUA_PM10': (4, 2)},  # Solid untuk PM10, putus-putus untuk BMUA
        palette='Reds'
        )
    #membuat judul plot
    line_PM10.set_title("Rata-rata Harian PM10", y=1.05)
    #nama sumbu x
    line_PM10.set_xlabel("Hari")
    #nama sumbu y
    line_PM10.set_ylabel("Konsentrasi (μg/m³)")
    #hasil plot
    st.pyplot(line_PM10.figure)

    #pembahasan
    st.markdown(
        """
            <div style="text-align: justify;"> 
                Konsentrasi harian PM2.5 menunjukkan wilayah urban (Wanshouxigong) terkonsentrasi di atas BMUA, sedangkan suburban dan urban cenderung di bawah nilai BMUA. 
                Nilai di atas BMUA menandakan pencemaran udara yang tinggi. Sementara itu, konsentrasi harian PM10 menunjukkan nilai di bawah standar BMU di seluruh stasiun. 
                Nilai standar BMUA diambil berdasarkan <i>Air Quality Standards</i> China dalam nilai Grade II (wilayah kota industrial maupun rural yang tidak dipantau khusus). 
            </div>
        """
        , unsafe_allow_html=True)

with Tab4:
    #menampilkan header
    st.header("Analisis Lanjutan: Clustering-based Binning")
    #tampilkan dataframe
    st.write("Data Rata-Rata Bulanan PM2.5, PM10, dan O₃")
    st.dataframe(vis_cat)
    #plot boxplot
    #visualisasi
    for keterangan in vis_cat['Keterangan'].unique():
        plt.figure(figsize=(10,5))
        barplot_cat = sns.barplot(
            data=vis_cat[vis_cat['Keterangan'] == keterangan],
            x='Kategori', y='Jumlah', hue='Station',
            palette='hls', errorbar= None,  order= ['High', 'Medium', 'Low']
        )
        plt.title(f"{keterangan}")
        plt.ylabel("Jumlah Bulan")
        plt.tight_layout()
        plt.show()
        st.pyplot(fig=plt.gcf())
        plt.clf()
    #pembahasan
    st.markdown(
        """
            <div style="text-align: justify;">
                Kategori data menunjukkan bahwa konsentrasi PM2.5 dan PM10 secara berturut-turut cenderung memiliki nilai lebih tinggi di wilayah urban (Wanshouxigong), 
                suburban (Changping), dan rural (Huairou). Sebaliknya, O3 secara berturut-turut memiliki nilai lebih tinggi di wilayah rural (Huairou), suburban (Changping), 
                dan urban (Wanshouxigong).
            </div>
        """
        , unsafe_allow_html=True)
st.markdown("---")
st.header("Kesimpulan")
st.markdown(
    """
        <div style="text-align: justify;">
            1. Pola bulanan PM2.5 dan PM10 menunjukkan konsentrasi lebih banyak di awal dan akhir tahun, sedangkan polutan O₃ pada musim kering (Juni-Juli-Agustus).
            <br>
            2. Pola diurnal PM2.5 dan PM10 menunjukkan konsentrasi lebih banyak di malam hari dengan pola cenderung konstan, sedangkan O₃ puncak konsentrasinya di siang hari.
            <br>
            3. Konsentrasi harian PM2.5 menunjukkan wilayah urban berpolusi tinggi dengan konsentrasi di atas BMUA, sedangkan PM10 menunjukkan nilai di bawah BMUA di seluruh stasiun.
            <br>
            4. Konsentrasi PM2.5 dan PM10 secara berturut-turut cenderung memiliki nilai lebih tinggi di wilayah urban (Wanshouxigong), sedangkan O₃ lebih banyak di wilayah rural (Huariou).
 
        </div>
    """
        , unsafe_allow_html=True)

