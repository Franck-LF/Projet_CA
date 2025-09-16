

import streamlit as st
import base64
import streamlit as st
from pdf2image import convert_from_path

from streamlit_pdf_viewer import pdf_viewer



path = """C:/Users/Utilisateur/Documents/Projet_CA/PDF/"""
pdf_file = path + "image.pdf"

uploaded_file = st.file_uploader(pdf_file, type="pdf")


cols = st.columns(3)

with cols[0]:
    st.title("📄 Affichage direct du PDF dans Streamlit")

    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Afficher dans un iframe
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)
    st.write("Test1")



with cols[1]:
    st.title("🖼️ Affichage du PDF converti en images")

    # Charger et convertir le PDF en images (toutes les pages)
    # pages = convert_from_path(pdf_file, dpi=150)

    # Afficher chaque page
    # for i, page in enumerate(pages):
    #     st.image(page, caption=f"Page {i+1}", use_column_width=True)
    st.write("Test2")



with cols[2]:
    st.title("Avec PDF Viewer")

    pdf_viewer(pdf_file)
