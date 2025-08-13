import shutil
import os
from block_markdown import markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")



def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def extract_title(markdown):
    md_lines = markdown.split("\n")
    for line in md_lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    f.close()
    with open(template_path) as t:
        template = t.read()
    t.close()
    node = markdown_to_html_node(md)
    HTML_string = node.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", HTML_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as d:
        d.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with open(template_path) as t:
        template = t.read()
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        target_path = os.path.join(dest_dir_path, filename)
        if not os.path.exists(target_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        if not os.path.isfile(file_path):
            generate_pages_recursive(file_path, template_path, target_path)
        else:
            with open(file_path) as f:
                md = f.read()
            node = markdown_to_html_node(md)
            HTML_string = node.to_html()
            title = extract_title(md)
            template_copy = template.replace("{{ Title }}", title)
            template_copy = template_copy.replace("{{ Content }}", HTML_string)
            with open(os.path.join(dest_dir_path, "index.html"), 'w') as d:
                    d.write(template_copy)


if __name__ == "__main__":
    main()