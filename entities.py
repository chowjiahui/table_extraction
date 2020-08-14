from typing import List


class Position:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.x1 = float(xmin)
        self.x2 = float(xmax)
        self.y1 = float(ymin)
        self.y2 = float(ymax)

    @property
    def midpoint(self):
        mp_x = (self.x2 + self.x1) / 2
        mp_y = (self.y2 + self.y1) / 2
        return Midpoint(mp_x, mp_y)

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def width(self):
        return self.x2 - self.x1


class Midpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    def __init__(self, pos: Position, text):
        self.pos = pos
        self.text = text

    def __str__(self):
        return f"Text: {self.text} \nPositions: {self.pos.__dict__}\n" \
               f"Midpoints: {self.pos.midpoint.__dict__}"

    def x_overlaps(self, other_pos: Position):
        other_inner = self.pos.x1 <= other_pos.x1 <= self.pos.x2 or self.pos.x1 <= other_pos.x2 <= self.pos.x2
        other_outer = other_pos.x1 <= self.pos.x1 <= other_pos.x2 or other_pos.x1 <= self.pos.x2 <= other_pos.x2
        return other_inner or other_outer


class Page:
    def __init__(self, _id: str, blocks: List[Block], height, width):
        self.id = _id
        self.blocks = blocks
        self.height = height
        self.width = width


class Header:
    def __init__(self, start_block: Block):
        self.blocks = [start_block]
        self.pos = Position(start_block.pos.x1, start_block.pos.x2,
                            start_block.pos.y1, start_block.pos.y2)

    @property
    def titles(self):
        return [block.text for block in self.blocks]

    def add(self, block: Block):
        self.blocks.append(block)
        self.combine_pos(block.pos)

    def combine_pos(self, block_pos: Position):
        if block_pos.x2 > self.pos.x2:
            self.pos.x2 = block_pos.x2
        if block_pos.y2 > self.pos.y2:
            self.pos.y2 = block_pos.y2

        if block_pos.x1 < self.pos.x1:
            self.pos.x1 = block_pos.x1
        if block_pos.y1 < self.pos.y1:
            self.pos.y1 = block_pos.y1


class Row:
    def __init__(self, header: Header, block: Block, col_name):
        self.values = {title: "" for title in header.titles}
        self.min_y = block.pos.y1
        self.max_y = block.pos.y2
        self.add(block, col_name)

    def update_range(self, block):
        def inequality(mp_y):
            return min(self.min_y, block.pos.y1) < mp_y < max(self.max_y, block.pos.y2)
        return inequality

    def add(self, block, col_name):
        self.y_overlaps = self.update_range(block)
        val = self.values.get(col_name)
        if not val:
            self.values[col_name] = block.text
        else:
            self.values[col_name] += ("|" + block.text)


class Table:
    def __init__(self, title: str, header: Header, rows: List[Row]):
        self.title = title
        self.header = header
        self.rows = rows
