import os
import subprocess
from subprocess import PIPE
from bs4 import BeautifulSoup

from entities import Position, Block, Page


class PDFExtractor:

    def __init__(self, html_output_folder):
        self.output_folder = html_output_folder

    def extract(self, pdf_path):
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

        output_path = self.create_file_path(pdf_path, self.output_folder)
        if not os.path.exists(output_path):
            command = 'pdftotext -f 1 -l 1 -r 300 -nodiag -bbox-layout ' \
                      f'"{pdf_path}" "{output_path}"'
            result = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
            stdout = result.stdout.decode('utf-8')
            if stdout.strip():
                print(stdout)
                raise subprocess.CalledProcessError

        return self.extract_page(output_path)

    def create_file_path(self, pdf_path, output_folder):
        filename = os.path.split(pdf_path)[-1]
        return os.path.join(output_folder, filename)

    def extract_page(self, output_path):
        with open(output_path) as file:
            html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        html_blocks = soup.findAll("line")

        blocks = [self.to_block(tag) for tag in html_blocks]
        page_size = soup.find("page")
        height, width = self.to_height_width(page_size)

        file_id = os.path.split(output_path)[-1]
        return Page(_id=file_id, blocks=blocks, height=height, width=width)

    def to_block(self, tag):
        pos = Position(**tag.attrs)
        clean_text = tag.text.strip().replace("\n", " ")
        return Block(pos, clean_text)

    def to_height_width(self, page_size):
        return float(page_size.attrs['height']), float(page_size.attrs['width'])
