import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd

# Set Tesseract path

st.title("AI Invoice Auditor")

st.write("Upload an invoice to detect billing errors.")

uploaded_file = st.file_uploader("Upload Invoice", type=["png","jpg","jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Invoice")

    text = pytesseract.image_to_string(image)

    st.subheader("Extracted Text")

    st.write(text)

    issues = []

    if "fuel surcharge" in text.lower():
        issues.append("Fuel surcharge detected – verify contract")

    if "handling fee" in text.lower():
        issues.append("Unauthorized handling fee detected")

    if "gst 28%" in text.lower():
        issues.append("GST rate might be incorrect")

    st.subheader("Audit Result")

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("No discrepancies detected")

    data = {
        "Issue":["Rate mismatch","Duplicate invoice","GST error"],
        "Estimated Loss":[15000,10000,5000]
    }

    df = pd.DataFrame(data)

    st.subheader("Overcharge Summary")


    st.bar_chart(df.set_index("Issue"))
