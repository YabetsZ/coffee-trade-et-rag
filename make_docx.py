from html2docx import html2docx

with open("PROJECT_DOCUMENTATION.html", "r") as f:
    html_content = f.read()

html2docx(html_content, "PROJECT_DOCUMENTATION.docx")
print("Saved DOCX file")
