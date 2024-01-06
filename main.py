# pdf generate
from data_process.aritmetics import pdf, MainBoard, CurrentSaw, Cuts, Divider, MadeBoards, Incisions, SortedAvailableBoards, ProjectProperties

def set_header(pdf):
    def header():
        pdf.set_y(10)
        pdf.set_font('Arial', style= 'B', size=14)
        pdf.cell(0, pdf.CellHeight, txt=ProjectProperties['Title'], ln=1)
        pdf.set_line_width(0.1)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.header = header

def add_title_content():
    if ProjectProperties['ProjectNotes'] != 'No notes':
        pdf.set_font_size(8)
        pdf.multi_cell(pdf.AvailableWidth, pdf.CellHeight, ProjectProperties['ProjectNotes'])

def add_main_board_content():
    if MainBoard.generate == True:
        pdf.set_font_size(12)
        pdf.cell(0, pdf.CellHeight, MainBoard.label , ln=1)
        pdf.set_font_size(8)
        if MainBoard.real_valueZ != 18:
            pdf.cell(0, 5, str(MainBoard.valueZ), ln=1)
        if MainBoard.notes != 'No notes':
            pdf.multi_cell(0, 5, MainBoard.notes)
        if MainBoard.real_valueX != 2800 or MainBoard.real_valueY != 2070:
            pdf.set_font_size(6)
            pdf.set_x(pdf.Center - 10) # offset
            pdf.cell(0, 5, str(MainBoard.real_valueX) + ' x ' + str(MainBoard.real_valueY), ln=1)
        y = pdf.get_y()
        generation(Divider, MadeBoards, Incisions, y)
        return SortedAvailableBoards

def generation(div, madeboards, incisions, offset_y):
    mainboardwidth = MainBoard.real_valueX / div
    mainboardheight = MainBoard.real_valueY / div
    MainBoardposX = pdf.Center - (mainboardwidth / 2)
    page_subtract = 0
    # page setup aritmetics
    for i in range(pdf.MainBoardCount): # ?
        y = offset_y + i * (mainboardheight + pdf.CellHeight) - page_subtract
        # if another rect goes out of the page
        if y + (mainboardheight) > pdf.AvailableHeight:
            pdf.add_page()
            y = offset_y = pdf.t_margin + pdf.header_size
            page_subtract = i * (mainboardheight + pdf.CellHeight)
        pdf.rect(MainBoardposX, y, mainboardwidth, mainboardheight)
        posx, posy = generate_crops(div, mainboardheight, mainboardwidth, MainBoardposX, y)
        generate_contents(posx, posy, madeboards, incisions, i + 1)
        if i == pdf.MainBoardCount - 1: # if last itiration
            pdf.set_xy(pdf.l_margin, y + mainboardheight + pdf.CellHeight)

def generate_contents(x, y, madeboards, incisions, i):
    for rect in madeboards:
        if rect.mainboard == i:
            pdf.rect(rect.posX + x, rect.posY + y, rect.valueX, rect.valueY)
            pdf.set_xy(rect.posX + x + (rect.valueX / 2) - 5, rect.posY + y + (rect.valueY / 2) - 2.5) # set to middle - rannum so it is 'centered'
            pdf.set_font_size(5)
            pdf.cell(0, 5, str(rect.real_valueX) + ' x ' + str(rect.real_valueY))
    for line in incisions:
        if line.mainboard == i:
            pdf.line(line.posX + x, line.posY + y, line.posX2 + x, line.posY2 + y)   

def generate_crops(div, mainboardheight, mainboardwidth, x, y):
    #crop gen + xy offset
    crop = pdf.Crop / div
    pdf.dashed_line(x + crop, y, x + crop, y + mainboardheight)
    pdf.dashed_line(x, y + crop, x + mainboardwidth, y + crop)
    return x + crop, y + crop      

def add_saw_content():
    if CurrentSaw.generate == True:
        pdf.set_font_size(12)
        pdf.cell(0, pdf.CellHeight, CurrentSaw.label, ln=1)
        if CurrentSaw.real_valueX != 3 or CurrentSaw.notes != 'No notes':
            pdf.set_font_size(8)
            pdf.multi_cell(0, pdf.CellHeight, 'Saw width: ' + str(CurrentSaw.real_valueX) + '\n' + CurrentSaw.notes)

def add_cuts_content():
    notgenerated = 0
    offset_x = 6
    offset_y = 1.4
    for each in Cuts:
        if each.generate == True:
            cut_page_check(each)       
            pdf.set_font_size(12)
            pdf.cell(0, pdf.CellHeight, each.label, ln=0)
            # if there is count generate it on the same line as label
            if each.count != 1:
                x = pdf.r_margin + pdf.get_string_width(each.label) + 2
                pdf.set_x(x)
                pdf.set_font_size(8)
                pdf.cell(0, pdf.CellHeight, str(each.count) + 'x', ln=1)
            # else add line so that notes/cuts are generated on a new one
            else:
                pdf.set_y(pdf.get_y() + 5)
            if each.notes != 'No notes':
                pdf.set_font_size(8)
                pdf.cell(0, 5, each.notes, ln=1)

            y = pdf.get_y()
            pdf.set_font_size(6)
            pdf.rect(pdf.Center - (each.valueX / 2), y, each.valueX, each.valueY)
            pdf.set_xy(pdf.Center - offset_x, y + (each.valueY / 2) - offset_y)
            pdf.cell(0, 5, str(each.real_valueX) + ' x ' + str(each.real_valueY))
            pdf.set_y(y + each.valueY + pdf.CellHeight)
        else:
            notgenerated += each.count
    if notgenerated != 0:
        print('Cuts not generated: ' + str(notgenerated))

def cut_page_check(cut):
    # count height of next cut
    y = pdf.get_y()
    height = pdf.CellHeight + cut.valueY # label
    if cut.notes != 'No notes':
        height += 5
    if y + height > pdf.AvailableHeight:
        pdf.add_page()

def add_leftover_cuts_content(leftovercuts):
    # leftovers filter
    if ProjectProperties['GenerateLC'] == True:
        for item in reversed(leftovercuts):
            if item.real_valueX < 80 or item.real_valueY < 80: #random number - if its size is bigger then 40x20 or similar types
                leftovercuts.remove(item)
        #content
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.set_y(pdf.get_y())
        pdf.set_font('Arial', 'I', 6)
        # compress leftovers 
        for cut in leftovercuts:
            cut.count = 1
        for cut in leftovercuts:
            for next_cut in reversed(leftovercuts):
                if next_cut != cut and cut.real_valueX == next_cut.real_valueX and cut.real_valueY == next_cut.real_valueY:
                    cut.count += 1
                    leftovercuts.remove(next_cut)

        # sort and print leftovers
        leftovercuts = sorted(leftovercuts, key=lambda obj: obj.real_valueX * obj.real_valueY, reverse=True)
        currentline = ''
        for i in range(len(leftovercuts)):
            valuestring = str(leftovercuts[i].real_valueX) + ' x ' + str(leftovercuts[i].real_valueY)
            if leftovercuts[i].count > 1:
                valuestring += ' ' + str(leftovercuts[i].count) + 'x'
            if pdf.get_string_width(currentline + valuestring) <= pdf.w - (pdf.l_margin * 2):
                currentline += valuestring + ', '
            else:
                pdf.cell(0, 5, currentline, ln=1)
        if currentline:
            pdf.cell(0, 5, currentline, ln=1)

set_header(pdf)
pdf.header()
add_title_content()
add_saw_content()
LeftoverCuts = add_main_board_content()
add_cuts_content()
add_leftover_cuts_content(LeftoverCuts)
# Save PDF to a file
pdf_filename = "CutApp.pdf"
pdf.output(pdf_filename)