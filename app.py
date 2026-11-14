import streamlit as st
import random

st.set_page_config(page_title="JTI Stant Vardiya Sihirbazı", page_icon="🎯", layout="wide")

st.title("🎯 JTI Stant Vardiya Sihirbazı")
st.write("Çalışanların müsaitliklerini sol menüden ayarla, özel kuralını seç ve butona basarak adil haftalık çizelgeyi anında cebine indir!")

# 1. Çalışan İsimleri (Büyük/Küçük Harf Düzenlenmiş)
kizlar = [
    "Fatma Çavuş",
    "Ece Balcı",
    "Tuğba Palacı",
    "Damla Nur Alp",
    "Irmak Arslan",
    "L. Hatun Varol",
    "Yağmur Günel"
]

gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi']

# Stantlar ve Sabit Süpervizör Kuralları
stantlar = {
    'Crash Stant': {'saat': '18:00 - 02:00', 'sup': 'Yiğit Yılmaz'},
    'Glenn Stant': {'saat': '17:00 - 01:00', 'sup': 'SPV'}
}

# 2. Yan Menüden Müsaitlik Belirleme
st.sidebar.header("🗓️ Çalışan Müsaitlik Günleri")
musaitlik = {}
for kiz in kizlar:
    musaitlik[kiz] = st.sidebar.multiselect(
        f"{kiz} Müsait Günler",
        gunler,
        default=gunler,
        key=f"m_{kiz}"
    )

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Özel / Sabit Atamalar")
sabit_gun = st.sidebar.selectbox("Özel Atama Yapılacak Gün (İsteğe Bağlı)", ["Yok"] + gunler)
sabit_stant = st.sidebar.selectbox("Hangi Stant?", list(stantlar.keys()))
sabit_kiz = st.sidebar.selectbox("Hangi Çalışan Kesin Orada Olsun?", kizlar)

# 3. Algoritma ve Çizelgeyi Oluşturma Butonu
if st.button("✨ Vardiya Çizelgesini Oluştur!", type="primary"):
    calisma_sayilari = {kiz: 0 for kiz in kizlar}
    cizelge = {gun: {} for gun in gunler}
    
    # Sabit atama varsa önce onu çakalım
    if sabit_gun != "Yok":
        sup_adi = stantlar[sabit_stant]['sup']
        cizelge[sabit_gun][sabit_stant] = {'kiz': sabit_kiz, 'sup': sup_adi}
        calisma_sayilari[sabit_kiz] += 1

    # Dağıtım motoru
    for gun in gunler:
        for stant, bilgi in stantlar.items():
            if stant in cizelge[gun]:
                continue
            
            # O gün müsait olan ve başka stantta olmayan çalışanları bul
            bosta_olanlar = []
            for k in kizlar:
                bugun_calisiyor = any(k == cizelge[gun][s].get('kiz') for s in cizelge[gun])
                if gun in musaitlik[k] and not bugun_calisiyor:
                    bosta_olanlar.append(k)
            
            if not bosta_olanlar:
                secilen_kiz = "⚠️ Uygun Kimse Yok!"
            else:
                # Adil dağılım: O ana kadar en az çalışanlara öncelik ver
                min_calisma = min(calisma_sayilari[k] for k in bosta_olanlar)
                adaylar = [k for k in bosta_olanlar if calisma_sayilari[k] == min_calisma]
                secilen_kiz = random.choice(adaylar)
                calisma_sayilari[secilen_kiz] += 1
            
            sup_adi = bilgi['sup']
            cizelge[gun][stant] = {'kiz': secilen_kiz, 'sup': sup_adi}

    # Sonuçları ekrana basalım
    st.success("JTI stant vardiya çizelgesi başarıyla hazırlandı şefim! 🎉")
    
    cols = st.columns(2)
    idx = 0
    for gun, gunluk_stantlar in cizelge.items():
        with cols[idx % 2]:
            st.subheader(f"📅 {gun}")
            for stant, bilgi in stantlar.items():
                saat = bilgi['saat']
                veri = gunluk_stantlar.get(stant, {})
                k = veri.get('kiz', 'Boş')
                s = veri.get('sup', '')
                st.markdown(f"- **{stant}** ({saat}): `✨ {k}` + 👔 **{s}**")
            st.markdown("---")
        idx += 1
        
    st.subheader("📊 Toplam Çalışma Günü Dağılımı (Adalet Kontrolü)")
    col_stats = st.columns(len(kizlar))
    for i, (kiz, sayi) in enumerate(calisma_sayilari.items()):
        with col_stats[i]:
            st.metric(label=kiz, value=f"{sayi} gün")
