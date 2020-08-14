from datetime import datetime
import locale

import pandas as pd

from entities import Page, Header, Row, Table
from pdf_extractor import PDFExtractor

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class TableExtractor:
    table_width_threshold = 2700
    compulsory_cols = ["Booking Date", "Txn Date"]

    def extract_table(self, page: Page):
        header = None
        row = None
        rows = []
        sorted_blocks = sorted(page.blocks, key=lambda blk: (blk.pos.midpoint.y, blk.pos.midpoint.x))
        for block in sorted_blocks:

            if header and self.is_ready(header):

                if row and row.y_overlaps(block.pos.midpoint.y):
                    col_name = self.find_col_name(block, header)
                    if col_name:
                        row.add(block, col_name)

                else:
                    if row:
                        rows.append(row)
                    col_name = self.find_col_name(block, header)
                    if col_name:
                        row = Row(header, block, col_name)

            elif not header:
                header = Header(start_block=block)
            elif header.pos.y1 <= block.pos.midpoint.y <= header.pos.y2:
                header.add(block)
            elif not self.is_ready(header):
                header = None

        table = Table(title=page.id, header=header, rows=rows)
        return self.postprocess(table)

    def find_col_name(self, block, header):
        for col in header.blocks:
            if block.x_overlaps(col.pos):
                return col.text

    def is_ready(self, header: Header):
        return header.pos.width > self.table_width_threshold

    def postprocess(self, table: Table):
        parsed_rows = []
        for row in table.rows:
            parsed_row = self.parse_row_datatype(row)
            if parsed_row.values:
                parsed_rows.append(parsed_row)
        table.rows = parsed_rows

        return self.process_rows(table, skip_last=True)

    def parse_row_datatype(self, row: Row):
        parsed_values = dict()
        for col, cell in row.values.items():
            if not cell:
                continue
            try:
                if "Date" in col:
                    datetime_cell = datetime.strptime(cell, '%d.%m.%Y')
                    cell = datetime_cell.strftime("%Y/%m/%d")
                elif "Text" not in col:
                    cell = locale.atof(cell)
                parsed_values[col] = cell

            except ValueError:
                print(f"Removed invalid cell: {cell}")
                continue
        row.values = parsed_values
        return row

    def process_rows(self, table: Table, skip_last):
        complete_row = None
        processed_rows = []
        rows = table.rows[:-1] if skip_last else table.rows
        for row in rows:
            if self.has_compulsory_cols(row):
                if complete_row:
                    processed_rows.append(complete_row)
                complete_row = row

            elif complete_row:
                complete_row = self.join_rows(row, complete_row)

        if complete_row:
            processed_rows.append(complete_row)
        processed_rows.append(table.rows[-1])
        table.rows = processed_rows
        return table

    def join_rows(self, row: Row, prev_row: Row):
        for col, cell in prev_row.values.items():
            if row.values.get(col):
                prev_row.values[col] = f"{prev_row.values[col]}\n{row.values[col]}"
        return prev_row

    def has_compulsory_cols(self, row: Row):
        return all(row.values.get(comp_col) for comp_col in self.compulsory_cols)

    @staticmethod
    def to_csv(table: Table, filepath):
        data = [row.values for row in table.rows]
        pd.DataFrame(data, columns=table.header.titles).to_excel(filepath, index=False)
        print(f"Table file saved to {filepath}!")
