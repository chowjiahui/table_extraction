import os

from pdf_extractor import PDFExtractor
from table_extractor import TableExtractor

if __name__ == '__main__':

    output_folder = "html_output"
    pdf_extractor = PDFExtractor(output_folder)

    html_file = "canopy_technical_test_output.html"
    out_pdf_path = os.path.join(output_folder, html_file)
    page = pdf_extractor.extract_page(out_pdf_path)

    table_extractor = TableExtractor()
    tbl = table_extractor.extract_table(page)

    out_table_path = "tables/canopy_technical_test_output.xlsx"
    table_extractor.to_csv(tbl, out_table_path)