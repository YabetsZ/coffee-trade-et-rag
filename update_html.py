from markdown import markdown

with open("PROJECT_DOCUMENTATION.md", "r") as f:
    text = f.read()

html_content = markdown(text, extensions=['tables', 'fenced_code'])

html_template = """<html><head><meta charset="UTF-8"><style>body { font-family: 'Arial', sans-serif; max-width: 850px; margin: 0 auto; padding: 40px; color: #000000; line-height: 1.6; background-color: #ffffff; } h1 { font-family: 'Arial', sans-serif; font-size: 26pt; text-align: center; margin-bottom: 20px; color: #1a1a1a; } h2 { font-size: 18pt; font-family: 'Arial', sans-serif; color: #2c3e50;  padding-bottom: 6px; margin-top: 40px; } h3 { font-size: 14pt; color: #34495e; margin-top: 30px; } p { font-size: 12pt; text-align: justify; margin-bottom: 15px; } ul, ol { font-size: 12pt; margin-bottom: 20px; padding-left: 30px; } li { margin-bottom: 10px; } pre { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 6px; font-family: 'Courier New', Courier, monospace; font-size: 10.5pt; overflow-x: auto; } code { font-family: 'Courier New', Courier, monospace; background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; font-size: 10.5pt; color: #d63384; } hr { border: 0; border-top: 1px solid #eaeaea; margin: 40px 0; } table { border-collapse: collapse; width: 100%; margin-bottom: 20px; } th, td { border: 1px solid #ddd; padding: 8px; text-align: left; } th { background-color: #f2f2f2; }</style></head><body>"""

full_html = html_template + html_content + "</body></html>"

with open("PROJECT_DOCUMENTATION.html", "w") as f:
    f.write(full_html)
