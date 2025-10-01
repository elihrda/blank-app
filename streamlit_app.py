import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="Kružnice – generátor bodů", layout="centered")

st.sidebar.header("Parametry kružnice")
x0 = st.sidebar.number_input("Střed X [m]", value=0.0, step=0.1)
y0 = st.sidebar.number_input("Střed Y [m]", value=0.0, step=0.1)
r = st.sidebar.number_input("Poloměr r [m]", value=5.0, step=0.1, min_value=0.1)
n = st.sidebar.slider("Počet bodů", min_value=3, max_value=500, value=20)
barva = st.sidebar.color_picker("Barva bodů", "#ff0000")

i = np.arange(n)
theta = 2 * np.pi * i / n
x = x0 + r * np.cos(theta)
y = y0 + r * np.sin(theta)

x_closed = np.append(x, x[0])
y_closed = np.append(y, y[0])

fig, ax = plt.subplots(figsize=(6,6))
ax.plot(x_closed, y_closed, marker="o", color=barva, linestyle="-")
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.grid(True)
ax.set_title(f"Kružnice se {n} body")

st.pyplot(fig)

df = pd.DataFrame({"x [m]": x, "y [m]": y})
st.dataframe(df)

with st.expander("Informace o autorovi a použitých technologiích"):
    st.write("""
    **Autor:** Eliška Hrdá
    **Kontakt:** 277870@vutbr.cz

    **Použité technologie:**  
    - [Streamlit](https://streamlit.io/) pro vývoj webové aplikace  
    - [NumPy](https://numpy.org/) pro výpočty  
    - [Matplotlib](https://matplotlib.org/) pro graf  
    - [Pandas](https://pandas.pydata.org/) pro tabulku dat  
    - [ReportLab](https://www.reportlab.com/) pro export do PDF  
    """)

def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Generátor bodů na kružnici", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Parametry:", styles["Heading2"]))
    elements.append(Paragraph(f"Střed: ({x0}, {y0}) m", styles["Normal"]))
    elements.append(Paragraph(f"Poloměr: {r} m", styles["Normal"]))
    elements.append(Paragraph(f"Počet bodů: {n}", styles["Normal"]))
    elements.append(Paragraph(f"Barva bodů: {barva}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Autor: Vaše jméno", styles["Normal"]))
    elements.append(Paragraph("Kontakt: váš@email.cz", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

if st.button("Exportovat do PDF"):
    pdf = create_pdf()
    st.download_button(
        label="Stáhnout PDF",
        data=pdf,
        file_name="kruznice.pdf",
        mime="application/pdf"
    )
