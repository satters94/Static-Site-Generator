import shutil
import os
from textnode import TextNode 
from textnode import TextType
from htmlnode import HTMLNode
from htmlnode import LeafNode
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title
from pathlib import Path

import sys

public_filepath = "./public"
static_filepath = "./static"
content_filepath = "./content"
template_filepath = "./template.html"
docs_filepath = "./docs"
default_basepath = "/"


def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    src_to_dest(static_filepath, docs_filepath)
    generate_page_recursive(content_filepath, template_filepath, docs_filepath, basepath)

def src_to_dest(src_path, dest_path):

    try:
        shutil.rmtree(dest_path)
        print(f"Folder '{dest_path}' and its contents deleted successfully.")
    except FileNotFoundError:
        print(f"Error: Folder '{dest_path}' not found.")
    except Exception as e:
        print(f"Error deleting folder '{dest_path}': {e}")
    
    try:
            shutil.copytree(src_path, dest_path)
            print("Folder copied successfully!")
    except FileExistsError:
            print("Destination folder already exists.")
    except Exception as e:
            print(f"An error occurred: {e}")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    markdown = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    html_string = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    html_page = html_page.replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
          os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w") as file:
            file.write(html_page)
            file.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
      content_tree = os.listdir(dir_path_content)    
      
      for node in content_tree:
            node_filepath = os.path.join(dir_path_content, node)
            dest_filepath = os.path.join(dest_dir_path, node)
            if os.path.isfile(node_filepath) and ".md" in node_filepath:
                  dest_filepath = Path(dest_filepath).with_suffix(".html")
                  generate_page(node_filepath, template_path, dest_filepath, basepath)
            else:
                dest_filepath = os.path.join(dest_dir_path, node)
                generate_page_recursive(node_filepath, template_path, dest_filepath, basepath)


main()
