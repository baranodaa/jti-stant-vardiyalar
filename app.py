import streamlit as st
import random

st.set_page_config(page_title="JTI Stant Vardiya Sihirbazı", page_icon="🎯", layout="wide")

st.title("🎯 JTI Stant Vardiya Sihirbazı")
st.write("Kızların müsaitliklerini sol menüden ayarla, özel kuralını seç ve butona basarak adil haftalık çizelgeyi anında cebine indir!")

# 1. Temel Tanımlamalar
kizlar = [f"kiz{i}" for i in range(1, 8)]
gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi']
stantlar = {
    'Crash Stant': '18:00 - 02:00',
    'Glenn Stant': '17:00 - 01:00'
}

# 2. Yan Menüden Müsaitlik Belirleme
st.sidebar.header("🗓️ Kızların Müsaitlik Günleri")
musaitlik = {}
for kiz in kizlar:
    # Varsayılan olarak her kız haftanın 6 günü müsait başlasın, sen istediğini kaldırabilirsin
    musaitlik[kiz] = st.sidebar.multiselect(
        f"{kiz.upper()} Müsait Günler",
        gunler,
        default=gunler
    )

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Özel / Sabit Atamalar")
sabit_gun = st.sidebar.selectbox("Özel Atama Yapılacak Gün (İsteğe Bağlı)", ["Yok"] + gunler)
sabit_stant = st.sidebar.selectbox("Hangi Stant?", list(stantlar.keys()))
sabit_kiz = st.sidebar.selectbox("Hangi Kız Kesin Orada Olsun?", kizlar)

# 3. Algoritma ve Çizelgeyi Oluşturma Butonu
if st.button("✨ Vardiya Çizelgesini Oluştur!", type="primary"):
    calisma_sayilari = {kiz: 0 for kiz in kizlar}
    cizelge = {gun: {} for gun in gunler}
    
    # Sabit atama varsa önce onu çakalım
    if sabit_gun != "Yok":
        cizelge[sabit_gun][sabit_stant] = sabit_kiz
        calisma_sayilari[sabit_kiz] += 1

    # Dağıtım motoru
    for gun in gunler:
        for stant in stantlar.keys():
            if stant in cizelge[gun]:
                continue
            
            # O gün müsait olan ve o gün başka stantta olmayan kızları bul
            bosta_olanlar = []
            for k in kizlar:
                bugun_calisiyor = k in cizelge[gun].values()
                if gun in musaitlik[k] and not bugun_calisiyor:
                    bosta_olanlar.append(k)
            
            if not bosta_olanlar:
                cizelge[gun][stant] = "⚠️ Uygun Kız Yok!"
                continue
            
            # Adil dağılım: O ana kadar en az çalışan kızlara öncelik ver
            min_calisma = min(calisma_sayilari[k] for k in bosta_olanlar)
            adaylar = [k for k in bosta_olanlar if calisma_sayilari[k] == min_calisma]
            
            secilen = random.choice(adaylar)
            cizelge[gun][stant] = secilen
            calisma_sayilari[secilen] += 1

    # Sonuçları ekrana basalım
    st.success("JTI stant vardiya çizelgesi başarıyla hazırlandı şefim! 🎉")
    
    # Günleri yan yana iki sütun halinde şık gösterelim
    cols = st.columns(2)
    idx = 0
    for gun, gunluk_stantlar in cizelge.items():
        with cols[idx % 2]:
            st.subheader(f"📅 {gun}")
            for stant, saat in stantlar.items():
                kiz = gunluk_stantlar.get(stant, "Boş")
                st.markdown(f"- **{stant}** ({saat}): `✨ {kiz}` + [Süpervizör]")
            st.markdown("---")
        idx += 1
        
    st.subheader("📊 Toplam Çalışma Günü Dağılımı (Adalet Kontrolü)")
    col_stats = st.columns(len(kizlar))
    for i, (kiz, sayi) in enumerate(calisma_sayilari.items()):
        with col_stats[i]:
            st.metric(label=kiz.upper(), value=f"{sayi} gün")v