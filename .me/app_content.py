import os

# Define folders based on user inputs
templates_folder = "../budgecument_root/budgecument/templates/bank_accounts"
apps_folder = "../budgecument_root/budgecument/apps/bank_accounts"
static_folder = "../budgecument_root/budgecument/static"

# Output file location
output_file = "../budgecument_root/.me/file_contents.txt"

# Initialize list to store file contents
file_contents = []

# Python files in the apps folder
python_files = ["models.py", "forms.py", "views.py", "urls.py"]

for file_name in python_files:
    file_path = os.path.join(apps_folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()  # Eksik olan satır
            file_contents.append(
                f"#####################################################\n\n"
                f"File Name: {file_name}\nFile Path: {file_path}\n\n{content}\n\n"
            )

# HTML files in the templates folder
for root, _, files in os.walk(templates_folder):
    for file_name in files:
        if file_name.endswith(".html"):
            file_path = os.path.join(root, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                file_contents.append(
                    f"#####################################################\n\n"
                    f"File Name: {file_name}\nFile Path: {file_path}\n\n{content}\n\n"
                )

# CSS and JS files in the static folder
static_files = ["css/styles.css", "js/app.js"]
for file_name in static_files:
    file_path = os.path.join(static_folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            file_contents.append(
                f"#####################################################\n\n"
                f"File Name: {file_name}\nFile Path: {file_path}\n\n{content}\n\n"
            )

# Add base.html file content
base_html_path = "../budgecument/templates/base.html"
if os.path.exists(base_html_path):
    with open(base_html_path, "r", encoding="utf-8") as file:
        content = file.read()
        file_contents.append(
            f"#####################################################\n\n"
            f"File Name: base.html\nFile Path: {base_html_path}\n\n{content}\n\n"
        )

# Write collected contents to the output file
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n\n".join(file_contents))

print(f"Dosyalar başarıyla '{output_file}' yoluna yazıldı.")
