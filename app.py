from dotenv import load_dotenv
load_dotenv()

import base64, io
import streamlit as st
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pdf2image import convert_from_bytes
import json

llm= ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0
)

System_Extration_rules="""
If user askes to extract invoices information, return ONLY valid JSON with:

{
  "invoice_number": "",
  "bill_to": "",
  "ship_to": "",
  "date": "",
  "total_amount": "",
  "currency": "",
  "tax_amount": "",
  "vendor_name": "",
  "vendor_address": "",
  "line_items": [
      {
         "description": "",
         "quantity": "",
         "unit_price": "",
         "amount": ""
      }
   ]
}

Rules:
- Do NOT include a field if it wasn't found.
- Do NOT include empty strings.
- For line_items: only include fields found for each line item.
- JSON ONLY. No extra text.
"""

base_system_instruction="""
You are an expert in understanding invoices. We will upload an image as an invoice, 
and you will have to answer any questions based on the uploaded image.
"""

def pdf_to_image_b64(uploaded_file):
    uploaded_file.seek(0)
    pdf_bytes= uploaded_file.read()

    pages = convert_from_bytes(pdf_bytes, poppler_path=r"C:\poppler-25.12.0\Library\bin")
    first_page= pages[0]

    buffer = io.BytesIO()
    first_page.save(buffer, format="PNG")

    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}", "image/png"

def file_bytes(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No file uploaded")
    
    if uploaded_file.type == "application/pdf":
        return pdf_to_image_b64(uploaded_file)

    uploaded_file.seek(0)
    bytes_data = uploaded_file.read()
    mime = uploaded_file.type
    b64 = base64.b64encode(bytes_data).decode('utf-8')
    return f"data:{mime};base64,{b64}", mime


def get_response(input_text, image_base64_url, file_type):
    if "extract" in input_text.lower():
        system_prompt= System_Extration_rules
    else:
        system_prompt= base_system_instruction

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[
            {"type": "text", "text": input_text},
            {
                "type": "image_url",
                "image_url": {"url": image_base64_url, "mime_type": file_type}
            }
        ])
    ]
    try:
        response = llm.invoke(messages)
        return response.content
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def clean_json_output(text: str) -> str:
    if not text:
        return text
    text = text.replace("```json", "")
    text = text.replace("```", "")
    
    return text.strip()

st.title("📄 MultiLanguage Invoice Extractor")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Invoice")
    uploaded_file = st.file_uploader(
        "Upload an invoice file",
        type=["jpg","jpeg","png","webp","pdf"]
    )

with col2:
    st.subheader("Instruction / Query")
    input = st.text_input(
        "What do you want to extract or ask?",
        key="input"
    )

st.markdown("---")

image=None

if uploaded_file is not None:
    if uploaded_file.type != "application/pdf":
        file_type = uploaded_file.type
        image= Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", width="content")
    else:
        st.info("PDF Uploaded - Preview not available")

submit = st.button("Analyze File")

if submit:
    if uploaded_file is None:
        st.error("Please upload an invoice image.")
    elif not input or input.strip() == "":
        st.error("Please enter a prompt/instruction about the invoice.")
    else:
        image_base64_url, file_type = file_bytes(uploaded_file)
        response = get_response(input, image_base64_url, file_type)

    try:
        cleaned = clean_json_output(response)
        parsed = json.loads(cleaned)
        st.subheader("📄 Extracted Invoice Data (Parsed JSON)")
        st.json(parsed)

        json_bytes = json.dumps(parsed, indent=4).encode("utf-8")
        st.download_button(
            "⬇️ Download JSON",
            data=json_bytes,
            file_name="invoice_data.json",
            mime="application/json"
        )

    except:
        st.subheader("📄 Raw Model Output (Not JSON)")
        st.code(response)





