import os

# Dosyaların bulunduğu klasörler (haftaici_root içinden yola başlayarak)
templates_folder = '../budgecument/templates/transactions/'
apps_folder = '../budgecument/apps/bank_accounts/'
static_folder = '../budgecument/static/'

# Dosya yolu ve içeriklerini saklamak için bir liste
file_contents = []

# apps klasöründeki Python dosyaları
python_files = ['models.py', 'forms.py', 'views.py', 'urls.py']

for file_name in python_files:
    file_path = os.path.join(apps_folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents.append(f"#####################################################\n\nFile Name: {file_name}\nFile Path: {file_path}\n\n{file.read()}\n\n")

# templates klasöründeki HTML dosyaları
html_files = []
for root, _, files in os.walk(templates_folder):
    for file_name in files:
        if file_name.endswith('.html'):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_contents.append(f"#####################################################\n\nFile Name: {file_name}\nFile Path: {file_path}\n\n{file.read()}\n\n")

# static klasöründeki CSS ve JS dosyaları
static_files = ['css/styles.css', 'js/app.js']
for file_name in static_files:
    file_path = os.path.join(static_folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents.append(f"#####################################################\n\nFile Name: {file_name}\nFile Path: {file_path}\n\n{file.read()}\n\n")

# base.html dosyasını eklemek
base_html_path = os.path.join('../budgecument/templates/', 'base.html')
if os.path.exists(base_html_path):
    with open(base_html_path, 'r', encoding='utf-8') as file:
        file_contents.append(f"#####################################################\n\nFile Name: base.html\nFile Path: {base_html_path}\n\n{file.read()}\n\n")


# Sonuçları bir metin dosyasına yazdırma
output_file = 'file_contents.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write('\n\n'.join(file_contents))

print(f"Dosyalar başarıyla '{output_file}' yoluna yazıldı.")
