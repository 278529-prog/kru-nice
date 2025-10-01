import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

st.set_page_config(page_title="Body na kružnici")

st.title("📍 Body na kružnici – webová aplikace")

# Sidebar pro vstupy
with st.sidebar:
    st.header("Parametry kružnice")
    stred_x = st.number_input("Střed X", value=0.0)
    stred_y = st.number_input("Střed Y", value=0.0)
    polomer = st.number_input("Poloměr [m]", value=5.0, min_value=0.1)
    pocet_bodu = st.slider("Počet bodů", min_value=3, max_value=500, value=8)
    barva = st.color_picker("Barva bodů", "#0000FF")
    vykreslit = st.button("▶️ Vykreslit kružnici")

# Funkce pro výpočet bodů
def vypocet_bodu(stred_x, stred_y, polomer, pocet_bodu):
    uhly = np.linspace(0, 2 * np.pi, pocet_bodu, endpoint=False)
    x = stred_x + polomer * np.cos(uhly)
    y = stred_y + polomer * np.sin(uhly)
    return x, y

if vykreslit:
    x, y = vypocet_bodu(stred_x, stred_y, polomer, pocet_bodu)

    # Vykreslení grafu
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(x, y, 'o', color=barva, label='Body na kružnici')
    ax.plot(stred_x, stred_y, 'r+', label='Střed')
    ax.set_aspect('equal')
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Textové výstupy
    st.subheader("Parametry:")
    st.write(f"Střed: ({stred_x}, {stred_y})")
    st.write(f"Poloměr: {polomer} m")
    st.write(f"Počet bodů: {pocet_bodu}")
    st.write(f"Barva: {barva}")

    # Generování PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    pdf.cell(200, 10, txt="Výstup – Body na kružnici", ln=True)
    pdf.cell(200, 10, txt=f"Střed: ({stred_x}, {stred_y})", ln=True)
    pdf.cell(200, 10, txt=f"Poloměr: {polomer} m", ln=True)
    pdf.cell(200, 10, txt=f"Počet bodů: {pocet_bodu}", ln=True)
    pdf.cell(200, 10, txt=f"Barva: {barva}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Souřadnice bodů:", ln=True)
    for i in range(pocet_bodu):
        pdf.cell(200, 10, txt=f"Bod {i+1}: ({x[i]:.2f}, {y[i]:.2f})", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Autor: Anna Nováková", ln=True)
    pdf.cell(200, 10, txt="Email: anna.novakova@student.cz", ln=True)

    # Uložení PDF
    nazev_souboru = "kruznice_vystup.pdf"
    pdf.output(nazev_souboru)

    # Stahovací tlačítko
    with open(nazev_souboru, "rb") as soubor:
        st.download_button(
            label="📄 Stáhnout PDF",
            data=soubor,
            file_name=nazev_souboru,
            mime="application/pdf"
        )

# Info okno
if st.button("ℹ️ O aplikaci"):
    st.info("""
    **Autor:** Anna Nováková  
    **Email:** anna.novakova@student.cz  
    **Technologie:** Python, Streamlit, Matplotlib, FPDF  
    Aplikace vykresluje body na kružnici, umožňuje výběr parametrů a export do PDF.
    """)
