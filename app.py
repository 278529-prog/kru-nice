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
    pocet_bodu = st.number_input("Počet bodů (3 až 500)", min_value=3, max_value=500, value=8, step=1)
    barva = st.color_picker("Barva bodů", "#0000FF")
    tlacitko = st.button("Vykreslit kružnici")

# Funkce pro výpočet bodů
def vytvor_bodove_body_na_kruhu(stred_x, stred_y, polomer, pocet_bodu):
    uhly = np.linspace(0, 2 * np.pi, pocet_bodu, endpoint=False)
    bod_x = stred_x + polomer * np.cos(uhly)
    bod_y = stred_y + polomer * np.sin(uhly)
    return bod_x, bod_y

# Vykreslení a PDF export
if tlacitko:
    bod_x, bod_y = vytvor_bodove_body_na_kruhu(stred_x, stred_y, polomer, pocet_bodu)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(bod_x, bod_y, 'o', color=barva, label=f'{pocet_bodu} bodů')
    ax.plot(stred_x, stred_y, 'r+', label="Střed")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # Tisk parametrů
    st.write(f"Střed: ({stred_x}, {stred_y})")
    st.write(f"Poloměr: {polomer} m")
    st.write(f"Počet bodů: {pocet_bodu}")
    st.write(f"Barva bodů: {barva}")

    # Vytvoření PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Výstup – Body na kružnici", ln=True)
    pdf.cell(200, 10, f"Střed: ({stred_x}, {stred_y})", ln=True)
    pdf.cell(200, 10, f"Poloměr: {polomer} m", ln=True)
    pdf.cell(200, 10, f"Počet bodů: {pocet_bodu}", ln=True)
    pdf.cell(200, 10, f"Barva: {barva}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, "Souřadnice bodů:", ln=True)
    for i in range(pocet_bodu):
        pdf.cell(200, 10, f"Bod {i+1}: ({bod_x[i]:.2f}, {bod_y[i]:.2f})", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, "Autor: Tvé jméno", ln=True)
    pdf.cell(200, 10, "Kontakt: tvůj-email@example.com", ln=True)

    # Uložení PDF
    pdf_file = "vystup_kruznice.pdf"
    pdf.output(pdf_file)

    # Nabídka ke stažení
    with open(pdf_file, "rb") as file:
        st.download_button(label="📄 Stáhnout PDF", data=file, file_name=pdf_file, mime="application/pdf")

# Informace o aplikaci v samostatném okně
if st.button("ℹ️ Informace o aplikaci"):
    st.info("""
    **Autor:** Tvé jméno  
    **Email:** tvůj-email@example.com  
    **Použité technologie:** Python, Streamlit, Matplotlib, FPDF  
    Aplikace umožňuje zobrazit body na kružnici dle zadaných parametrů, vykreslit je s osami a jednotkami a stáhnout výsledky jako PDF.
    """)
commit message
