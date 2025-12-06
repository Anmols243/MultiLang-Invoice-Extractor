🚀 Features
🔍 1. Invoice Extraction (Structured JSON Output)

Automatically extracts:

Invoice Number

Dates

Vendor Name & Address

Bill To / Ship To

Tax Amount

Currency

Total Amount

Line Items (description, quantity, unit price, amount)

🧠 2. Natural-Language Invoice Q&A

Ask questions like:

“What is the total amount?”

“Who is the vendor?”

“Extract all line items.”

“Translate the invoice details to English.”

📑 3. PDF Support

Converts the first page of any PDF to an image using pdf2image.

🌍 4. Multilingual Input

Queries in any language are supported.

💾 5. Downloadable Output

Download JSON (when extracted)

Download raw model output (fallback)

🛠️ Tech Stack
Component	Technology
LLM	Google Gemini 2.5 Pro Vision
Framework	Streamlit
LLM Framework	LangChain 1.x
File Processing	pdf2image, PIL
Config	python-dotenv
📦 Installation
1️⃣ Clone the repository
git clone https://github.com/Anmols243/Gemini
cd MultiLang_Invoice_Extractor

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your Gemini API key

Create a .env file:

GEMINI_API_KEY=your_api_key_here

5️⃣ Install Poppler (PDF to Image)

Windows users:
Download Poppler from:
https://github.com/oschwartz10612/poppler-windows/releases/

Update the path inside code if needed:

C:\poppler-25.12.0\Library\bin

▶️ Running the App
streamlit run app.py


Then open:

http://localhost:8501/

📁 Project Structure
├── app.py
├── .env
├── requirements.txt
├── README.md
└── (uploaded files at runtime)

🧩 How It Works (Overview)

User uploads an invoice (PNG/JPG/WebP/PDF).

File is converted to a base64 image.

LangChain sends:

System rules for extraction

User query

Invoice image

Gemini returns either:

Valid JSON (extraction)

Natural-language response (Q&A)

App displays results and enables download.

📤 Example Use Cases

Automated invoice data scraping

Bookkeeping automation

Multilingual invoice interpretation

Vendor bill processing

Finance document understanding