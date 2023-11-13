from fpdf import *
from datetime import datetime

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4') # 210 mm x 297 mm
        self.setup()

    def setup(self):
        self.add_page() # file start
        self.set_line_width(0.2)
        self.CellHeight = 7
        self.set_font('Arial', size=12)
        self.set_text_color(0,0,0)
        self.header_size = 2 * self.CellHeight
        self.footer_size = 15
        self.set_margins(10, 10 + self.header_size)
        self.b_margin = self.footer_size
        self.set_auto_page_break(auto=True, margin=self.b_margin)
        self.AvailableWidth = self.w - self.l_margin * 2
        self.AvailableHeight = self.h - self.t_margin - self.b_margin
        self.Center = self.w / 2
        self.Crop = 20
        self.MainBoardCount = 1
        self.title_set()

    def title_set(self):
        self.TITLE = 'CutApp'
        self.set_title(self.TITLE)

    def footer(self):
        self.set_y( - self.b_margin)
        self.set_font('Arial', style= 'I', size=8)
        self.cell(0, self.CellHeight, txt='Generated on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), align='C')
        self.cell(0, self.CellHeight, txt='Page %s' % self.page_no(), align='R')

pdf = PDF()