import os
import shutil
import sys
from generate_page import generate_page

def copy_static(source, destination):
    if not os.path.exists(source):
        print(f"Source {source} does not exist!")
        return
    
    if os.path.exists(destination):
        print(f"Cleaning destination: {destination}")
        shutil.rmtree(destination)
    
    os.makedirs(destination)

    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def main():
    # Par défaut la racine est "/", sauf si un argument est passé
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Pour GitHub Pages, on utilise souvent le dossier 'docs'
    dest_folder = "docs"

    print(f"--- Building for basepath: {basepath} ---")

    # 1. Copier les fichiers statiques vers docs
    print("--- Copying static files ---")
    copy_static("static", dest_folder)

    # 2. Générer toutes les pages récursivement vers docs
    print("--- Generating all pages ---")
    generate_pages_recursive("content", "template.html", dest_folder, basepath)
    
    print("--- Done! ---")

if __name__ == "__main__":
    main()