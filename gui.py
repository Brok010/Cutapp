# GUI creation - simple gui to get input information from a user
# TODO: value checks before save

from tkinter import *

from objects import Board, Saw, Cut #just to read basic values

class AutoScrollbar(Scrollbar):
   # A scrollbar that hides itself if it's not needed.
   # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")

class ScrollFrame:
    def __init__(self, master):
        self.vscrollbar = AutoScrollbar(master)
        self.vscrollbar.grid(row=0, column=1, sticky=N+S)
        self.hscrollbar = AutoScrollbar(master, orient=HORIZONTAL)
        self.hscrollbar.grid(row=1, column=0, sticky=E+W)
        self.canvas = Canvas(master, yscrollcommand=self.vscrollbar.set, 
                        xscrollcommand=self.hscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)
        # make the canvas expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        # create frame inside canvas
        self.frame = Frame(self.canvas)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)
        #added
        self.frame.bind("<Configure>", self.reset_scrollregion)

    def update(self):
        self.canvas.create_window(0, 0, anchor=NW, window=self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        if self.frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width = self.frame.winfo_reqwidth())
        if self.frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canvas.config(height = self.frame.winfo_reqheight())
    def reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

#globals
Coeficient = 2

def addcheckbox(frame, col, txt, checked):
    # Checkbox
    if checked == 1:
        checkboxbool = BooleanVar(value=True)
        cutframecheckbox = Checkbutton(frame, text=txt, variable=checkboxbool, onvalue=1, offvalue=0) 
    if checked == 0:
        checkboxbool = BooleanVar(value=False)
        cutframecheckbox = Checkbutton(frame, text=txt, variable=checkboxbool, onvalue=1, offvalue=0)

    cutframecheckbox.grid(row=0, column=col, sticky='e')
    return checkboxbool

Counter = 8
Cuts = []
def newframesetcontents(cut_frame):
    global Counter, Cuts
    # Frame title
    cut_frame_Label = Label(cut_frame, text="Cut " + str(Counter - 7), font=("Helvetica", 14))
    cut_frame_Label.grid(row=0, columnspan=3)
    # Checkbox
    check_box_bool_direction = addcheckbox(cut_frame, 3, 'Keep direction', 0)
    check_box_bool_generate = addcheckbox(cut_frame, 4, 'Generate', 1)
    # Contents labels
    cut_frame_label_entry1 = Label(cut_frame, text='Name')
    cut_frame_label_entry2 = Label(cut_frame, text='ValueX (mm)')
    cut_frame_label_entry3 = Label(cut_frame, text='ValueY (mm)')
    cut_frame_label_entry4 = Label(cut_frame, text='Notes')
    cut_frame_label_entry5 = Label(cut_frame, text='Count')
    cut_frame_label_entry1.grid(row=1, column=0)
    cut_frame_label_entry2.grid(row=1, column=1)
    cut_frame_label_entry3.grid(row=1, column=2)
    cut_frame_label_entry4.grid(row=1, column=3)
    cut_frame_label_entry5.grid(row=1, column=4)
    # Contents Entries
    cut_frame_entry1 = Entry(cut_frame)
    cut_frame_entry2 = Entry(cut_frame)
    cut_frame_entry3 = Entry(cut_frame)
    cut_frame_entry4 = Entry(cut_frame)
    cut_frame_entry5 = Entry(cut_frame)
    cut_frame_entry1.grid(row=2, column=0)
    cut_frame_entry2.grid(row=2, column=1)
    cut_frame_entry3.grid(row=2, column=2)
    cut_frame_entry4.grid(row=2, column=3)
    cut_frame_entry5.grid(row=2, column=4)
    # Add the Entry widgets to the list
    cut = {}
    cut['Name'] = cut_frame_entry1
    cut['ValueX'] = cut_frame_entry2
    cut['ValueY'] = cut_frame_entry3
    cut['Notes'] = cut_frame_entry4
    cut['Count'] =  cut_frame_entry5
    cut['Direction'] = check_box_bool_direction 
    cut['Generate'] = check_box_bool_generate
    Cuts.append(cut)
    Counter += 1

def addframes():
    #  New frame set up
    cut_frame = Frame(main_frame.frame, borderwidth=2, relief="groove")
    cut_frame.grid(row=Counter, column=0, columnspan=6)
    # New frame contents
    newframesetcontents(cut_frame)

main_board_vars = {}
saw_vars = {}
title_vars = {}

def addframecontents():
    # Title
        #frame creation
    title_frame = Frame(main_frame.frame)
    title_frame.grid(row=0, column=0,  sticky='w')
        #frame contents
    title_frame_label1 = Label(title_frame, text="Title", font=("Helvetica", 14))
    title_frame_label1.grid(row=0, column=0)
    title_frame_label2 = Label(title_frame, text="Notes", font=("Helvetica", 10))
    title_frame_label2.grid(row=0, column=1)
    title_frame_label3 = Label(title_frame, text='Coeficient: ')
    title_frame_label3.grid(row=0, column=2)
    title_frame_entry0 = Entry(title_frame)
    title_frame_entry0.grid(row=0, column=3)
    check_box_bool = addcheckbox(title_frame, 4, 'Generate leftover cuts', 1)
    title_frame_entry1 = Entry(title_frame)
    title_frame_entry1.grid(row=1, column=0)
    title_frame_entry2 = Entry(title_frame)
    title_frame_entry2.grid(row=1, column=1, columnspan=2, sticky="ew")
        # Spacer frame shenanigans - didnt find better solution
    title_spacer_frame = Frame(title_frame)
    title_spacer_frame.grid(row=1, column=3)
    title_frame.grid_columnconfigure(1, minsize=166) #just random num..
        # Create a button
    add_frame_button = Button(title_frame, text='Add cut', command=addframes)
    add_frame_button.grid(row=1, column=3, sticky='nsew')
    save_exit_button = Button(title_frame, text='Save & Exit', command=save_exit)
    save_exit_button.grid(row=1, column=4, sticky='nsew')
            # Add entries adresses to the list so i can work with them later
    title_vars['Coeficient'] = title_frame_entry0
    title_vars['Name'] = title_frame_entry1
    title_vars['Notes'] = title_frame_entry2
    title_vars['GenerateLC'] = check_box_bool
    
    # MainBoard
        #frame creation
    main_board_frame = Frame(main_frame.frame, borderwidth=2, relief="groove")
    main_board_frame.grid(row=1, column=0,  sticky='w')
        #frame contents
    main_board_frame_label = Label(main_board_frame, text="Main board", font=("Helvetica", 14))
    main_board_frame_label.grid(row=0, columnspan=5)
    main_board_frame_label_entry1 = Label(main_board_frame, text='Name')
    main_board_frame_label_entry1.grid(row=1, column=0)
    main_board_frame_label_entry2 = Label(main_board_frame, text='ValueX (mm)')
    main_board_frame_label_entry2.grid(row=1, column=1)
    main_board_frame_label_entry3 = Label(main_board_frame, text='ValueY (mm)')
    main_board_frame_label_entry3.grid(row=1, column=2)
    main_board_frame_label_entry4 = Label(main_board_frame, text='ValueZ (mm)')
    main_board_frame_label_entry4.grid(row=1, column=3)
    main_board_frame_label_entry5 = Label(main_board_frame, text='Notes')
    main_board_frame_label_entry5.grid(row=1, column=4, sticky="w")
    main_board_frame_entry1 = Entry(main_board_frame)
    main_board_frame_entry1.grid(row=2, column=0)
    main_board_frame_entry2 = Entry(main_board_frame)
    main_board_frame_entry2.grid(row=2, column=1)
    main_board_frame_entry3 = Entry(main_board_frame)
    main_board_frame_entry3.grid(row=2, column=2)
    main_board_frame_entry4 = Entry(main_board_frame)
    main_board_frame_entry4.grid(row=2, column=3)
    main_board_frame_entry5 = Entry(main_board_frame)
    main_board_frame_entry5.grid(row=2, column=4, sticky="ew")
        # Checkbox
    check_box_bool_direction = addcheckbox(main_board_frame, 3, 'Keep direction', 0)
    check_box_bool_generate = addcheckbox(main_board_frame, 4, 'Generate', 1)
        # Add entries adresses to the list so i can work with them later
    main_board_vars['Name'] = main_board_frame_entry1
    main_board_vars['ValueX'] = main_board_frame_entry2
    main_board_vars['ValueY'] = main_board_frame_entry3
    main_board_vars['ValueZ'] = main_board_frame_entry4
    main_board_vars['Notes'] = main_board_frame_entry5
    main_board_vars['Direction'] = check_box_bool_direction
    main_board_vars['Generate'] = check_box_bool_generate
    # Saw Board
        #frame creation
    saw_frame = Frame(main_frame.frame, borderwidth=2, relief="groove")
    saw_frame.grid(row=2, column=0,  sticky='w')
        #frame contents
    saw_frame_label = Label(saw_frame, text="Saw", font=("Helvetica", 14))
    saw_frame_label.grid(row=0, columnspan=5)
    saw_frame_label_entry1 = Label(saw_frame, text='Name')
    saw_frame_label_entry1.grid(row=1, column=0)
    saw_frame_label_entry2 = Label(saw_frame, text='ValueX (mm)')
    saw_frame_label_entry2.grid(row=1, column=1)
    saw_frame_label_entry3 = Label(saw_frame, text='Notes')
    saw_frame_label_entry3.grid(row=1, column=2, sticky='w')
    sasaw_frame_entry1 = Entry(saw_frame)
    sasaw_frame_entry1.grid(row=2, column=0)
    sasaw_frame_entry2 = Entry(saw_frame)
    sasaw_frame_entry2.grid(row=2, column=1)
    sasaw_frame_entry3 = Entry(saw_frame)
    sasaw_frame_entry3.grid(row=2, column=2, sticky='ew')
        # Checkbox
    check_box_bool = addcheckbox(saw_frame, 2, 'Generate', 1)
        # Add entries adresses to the list so i can work with them later
    saw_vars['Name'] = sasaw_frame_entry1
    saw_vars['ValueX'] = sasaw_frame_entry2
    saw_vars['Notes'] = sasaw_frame_entry3
    saw_vars['Generate'] = check_box_bool
        # Spacer frame shenanigans - didnt find better solution
    saw_spacer_frame = Frame(saw_frame)
    saw_spacer_frame.grid(row=2, column=3)
    saw_frame.grid_columnconfigure(2, minsize=371) #just random num..
    addframes()

Cuts_list = []
def save_exit():
    global ProjectProperties_dic, MainBoard_dic, Saw_dic, Cuts_list
    MainBoard = Board()
    SawInstance = Saw()
    # save
        # Retrieve user-entered values and update instances if provided
        # using.get() because of tkinter 'StringVars'
            # title
    title = title_vars['Name'].get() if title_vars['Name'].get() != '' else 'My Project'
    project_notes = title_vars['Notes'].get() if title_vars['Notes'].get() != '' else 'No notes'
    coeficient_var = float(title_vars['Coeficient'].get()) if title_vars['Coeficient'].get() != '' else Coeficient
    generate_LC = title_vars['GenerateLC'].get()
    ProjectProperties_dic = {'Title': title, 'ProjectNotes': project_notes, 'Coeficient': coeficient_var, 'GenerateLC': generate_LC} # leftover cuts
            # main board
    mainboard_label = main_board_vars['Name'].get() if main_board_vars['Name'].get() != '' else MainBoard.label
    mainboard_real_valueX = int(main_board_vars['ValueX'].get()) if main_board_vars['ValueX'].get() != '' else MainBoard.real_valueX
    mainboard_real_valueY = int(main_board_vars['ValueY'].get()) if main_board_vars['ValueY'].get() != '' else MainBoard.real_valueY
    mainboard_valueZ = int(main_board_vars['ValueZ'].get()) if main_board_vars['ValueZ'].get() != '' else MainBoard.real_valueZ
    mainboard_notes = main_board_vars['Notes'].get() if main_board_vars['Notes'].get() != '' else MainBoard.notes
    mainboard_generate = main_board_vars['Generate'].get()
    mainboard_direction = main_board_vars['Direction'].get()
    MainBoard_dic = {'Label': mainboard_label,'Real_valueX': mainboard_real_valueX,'Real_valueY': mainboard_real_valueY,'Real_valueZ': mainboard_valueZ,'Notes': mainboard_notes,'Generate': mainboard_generate,'Direction': mainboard_direction}
            # saw
    saw_label = saw_vars['Name'].get() if saw_vars['Name'].get() != '' else SawInstance.label
    saw_real_valueX = int(saw_vars['ValueX'].get()) if saw_vars['ValueX'].get() != '' else SawInstance.real_valueX
    saw_notes = saw_vars['Notes'].get() if saw_vars['Notes'].get() != '' else SawInstance.notes
    saw_generate = saw_vars['Generate'].get()
    Saw_dic = {'Label': saw_label,'Real_valueX': saw_real_valueX,'Notes': saw_notes, 'Generate': saw_generate}
            # cuts
    for cut in Cuts:
        CutInstance = Cut()
        cut_label = cut['Name'].get() if cut['Name'].get() != '' else CutInstance.label
        cut_real_valueX = int(cut['ValueX'].get()) if cut['ValueX'].get() != '' else CutInstance.real_valueX
        cut_real_valueY = int(cut['ValueY'].get()) if cut['ValueY'].get() != '' else CutInstance.real_valueY
        cut_notes = cut['Notes'].get() if cut['Notes'].get() != '' else CutInstance.notes
        cut_generate = cut['Generate'].get()
        cut_direction = cut['Direction'].get()
        cut_count = int(cut['Count'].get()) if cut['Count'].get() != '' else CutInstance.count
        cut_dic = {'Label': cut_label,'Real_valueX': cut_real_valueX,'Real_valueY': cut_real_valueY,'Notes': cut_notes,'Generate': cut_generate,'Direction': cut_direction, 'Count': cut_count}
        # add instances to a list
        Cuts_list.extend([cut_dic]) 
    # exit
    root.destroy()

# Window start
root = Tk()
root.title("CutApp")
main_frame = ScrollFrame(root)
addframecontents()
main_frame.update()
root.mainloop()