import fitz  # PyMuPDF
import re
import json
import os

def extract_relevant_pages(pdf_path, start_page=8):
    doc = fitz.open(pdf_path)
    text_by_page = []

    for page_num in range(start_page, len(doc)):
        text = doc[page_num].get_text("text")
        text_by_page.append(text)

    return text_by_page

def extract_section(text, start_marker, end_marker_list):
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return None
    start_idx += len(start_marker)

    end_idx = len(text)
    for marker in end_marker_list:
        temp_idx = text.find(marker, start_idx)
        if temp_idx != -1 and temp_idx < end_idx:
            end_idx = temp_idx

    return text[start_idx:end_idx].strip()

def clean_and_split_modules(text_by_page):
    full_text = "\n".join(text_by_page)
    modules = re.split(r'\n\s*Module title:\s*', full_text)
    cleaned_modules = []

    for module in modules[1:]:
        entry = {
            "module_title": None,
            "english_title": None,
            "language": None,
            "learning_outcomes": None,
            "contents": None
        }

        lines = module.split("\n")
        entry["module_title"] = lines[0].strip()
        module_text = "\n".join(lines)

        entry["english_title"] = extract_section(module_text, "Engl. module name:", ["Language:", "Intended learning outcomes", "Contents"])
        entry["language"] = extract_section(module_text, "Language:", ["Intended learning outcomes", "Contents", "Module coordinator:"])
        entry["learning_outcomes"] = extract_section(module_text, "Intended learning outcomes", ["Contents", "Module coordinator:", "Lecturer"])
        entry["contents"] = extract_section(module_text, "Contents", ["Module coordinator:", "Lecturer", "Recommended reading"])

        cleaned_modules.append(entry)

    return cleaned_modules

def save_as_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Update these paths to match your local files
pdf_paths = [
    "/Users/ritwikasen/Desktop/Digital Engineering/Modulkatalog_2024_Wintersemester-CourtesyTranslation.pdf",
    "/Users/ritwikasen/Desktop/Digital Engineering/Modulkatalog_2024_Sommersemester.pdf"
]

output_path = "/Users/ritwikasen/Desktop/Digital Engineering/Summer 2025/HCAI/HCAI Project/CurveMyPath/data/pdf_ovgucourses.json"

all_modules = []
for pdf in pdf_paths:
    raw_pages = extract_relevant_pages(pdf)
    modules = clean_and_split_modules(raw_pages)
    all_modules.extend(modules)

save_as_json(all_modules, output_path)
print(f"✅ Done. Parsed {len(all_modules)} modules and saved to {output_path}")
