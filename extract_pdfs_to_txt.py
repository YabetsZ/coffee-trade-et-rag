#!/usr/bin/env python3
"""Extract text from PDF files and save as .txt files in the corpus."""

from pathlib import Path
import pypdf

CORPUS_DIR = Path("data/corpus")


def normalize_pdf_text(text: str) -> str:
    """Clean up extracted PDF text."""
    cleaned = text
    cleaned = cleaned.replace("\x00", " ")
    cleaned = cleaned.replace("\u00ad", "")
    cleaned = cleaned.replace("…", " ")
    cleaned = cleaned.replace("::", ":")
    cleaned = cleaned.replace("‹", " ").replace("›", " ")
    cleaned = cleaned.replace("Ø", " ").replace("ø", " ")
    cleaned = cleaned.replace("፡", " ")
    cleaned = cleaned.replace("፤", "። ")
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def extract_pdf_to_txt(pdf_path: Path) -> None:
    """Extract text from a PDF and save as .txt file."""
    print(f"Processing {pdf_path.name}...")
    
    text_content = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, 1):
            extracted = page.extract_text()
            if extracted:
                normalized = normalize_pdf_text(extracted)
                if normalized:
                    text_content.append(normalized)
        
        full_text = "\n\n".join(text_content).strip()
        
        if full_text:
            # Save as .txt with same name
            txt_path = pdf_path.with_suffix(".txt")
            txt_path.write_text(full_text, encoding="utf-8")
            print(f"  ✓ Saved to {txt_path.name} ({len(full_text)} chars)")
        else:
            print(f"  ✗ No text extracted from {pdf_path.name}")
            
    except Exception as e:
        print(f"  ✗ Failed to process {pdf_path.name}: {e}")


def main():
    """Extract all PDFs in corpus directory."""
    pdf_files = list(CORPUS_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/corpus/")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s)\n")
    
    for pdf_path in sorted(pdf_files):
        extract_pdf_to_txt(pdf_path)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
