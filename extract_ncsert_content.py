# Step 1: PDF Text Extraction
import fitz  # PyMuPDF
def extract_chapter_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc):
        page_text = page.get_text()
        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
    return text

# Step 2: Call to LLM (e.g., OpenAI/Gemini)
import openai
def call_llm(prompt, chapter_text):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt + "\n" + chapter_text}],
        temperature=0.2
    )
    return completion.choices[0].message['content']

# Step 3: JSON to Excel Conversion
import json
import pandas as pd
def json_to_excel(json_data, excel_file):
    rows = []
    for topic in json_data['topics']:
        for sub in topic['subtopics']:
            for key, items in sub['content'].items():
                for item in items:
                    rows.append({
                        "Chapter": json_data['chapter_name'],
                        "Topic": topic['topic_name'],
                        "Sub-topic": sub['subtopic_header'],
                        "Content Type": key,
                        "Content": item.get('text', item),
                        "Page Number": item.get('page', '')
                    })
    pd.DataFrame(rows).to_excel(excel_file, index=False)
