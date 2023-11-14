import copy

from objects import Cut, Incision
from pdf_create import pdf
from data_get.data_load import MainBoard, CurrentSaw, Cuts, ProjectProperties

def Logic():
    Divider = find_divider()
    AvailableBoards, MadeBoards, Incisions = [], [], []
    AvailableBoards.append(create_available_boards(Divider, pdf.MainBoardCount))
    SortedCuts, SortedAvailableBoards = list_setup(Cuts, AvailableBoards, Divider)
    while SortedCuts != []:
        BoardFound = False
        CurrentCut = SortedCuts[-1]
        SortedAvailableBoards = sorted(SortedAvailableBoards, key=lambda obj: obj.valueX * obj.valueY)
        for each in SortedAvailableBoards: 
            CurrentBoard = each
            # gets smallest possible board to make the cut from
            # 1st line - if it can fit is given direction
            # 2nd 2 line - if it can be rotated and it fits
            if (CurrentBoard.valueX >= CurrentCut.valueX and CurrentBoard.valueY >= CurrentCut.valueY or
                CurrentBoard.valueX >= CurrentCut.valueY and CurrentBoard.valueY >= CurrentCut.valueX and CurrentCut.direction == False):
                SortedAvailableBoards.remove(each)
                BoardFound = True
                # set cut position to board position
                CurrentCut.posX = CurrentBoard.posX
                CurrentCut.posY = CurrentBoard.posY
                CurrentCut.mainboard = CurrentBoard.mainboard
                # TODO: crop reserves
                # if we need to rotate
                rotate = rotation_setup(CurrentCut, CurrentBoard, SortedCuts)
                if rotate == True: # if better to rotate
                    CurrentCut.valueX, CurrentCut.valueY = value_switch(CurrentCut.valueX, CurrentCut.valueY)
                    CurrentCut.real_valueX, CurrentCut.real_valueY = value_switch(CurrentCut.real_valueX, CurrentCut.real_valueY)
                # what cut to make first (True if its better to make horizontal cut first)
                v_cut = better_to_cut_h(CurrentCut, CurrentBoard, SortedCuts, CurrentSaw)
                # create the rectangle and the cut
                MadeBoards.append(copy.deepcopy(CurrentCut))
                CurrentSaw.valueX = CurrentSaw.real_valueX / Divider # kinda random line
                new_boards_creation(v_cut, CurrentCut, CurrentBoard, Incisions, SortedAvailableBoards)
                # since we found it we need to remove the cut
                if CurrentCut.count > 1:
                    CurrentCut.count -= 1
                else: 
                    SortedCuts.pop() # gets and removes last(biggest) cut from a list
                break
                
            # if we didnt find a board
        if BoardFound == False:
            pdf.MainBoardCount += 1
            NewBoard = create_available_boards(Divider, pdf.MainBoardCount) # in generation we need to set of x and y by a certain amount
            SortedAvailableBoards.append(NewBoard)
    return Divider, MadeBoards, Incisions, SortedAvailableBoards

def new_boards_creation(v_cut, currentcut, currentboard, incisions, sortedavailableboards):
    if v_cut == True:
        # vertical cut
        # Create the left over boards and put them in Available boards
        inc = Incision(currentboard.posX + currentcut.valueX, currentboard.posY, currentboard.posX + currentcut.valueX, currentboard.posY + currentboard.valueY, currentboard.mainboard)
        incisions.append(copy.deepcopy(inc))
        board1 = Cut(posX=currentboard.posX + currentcut.valueX + CurrentSaw.valueX,posY=currentboard.posY, mainboard=currentboard.mainboard,
                        valueX=currentboard.valueX - currentcut.valueX - CurrentSaw.valueX,valueY=currentboard.valueY,
                        real_valueX=currentboard.real_valueX - currentcut.real_valueX - CurrentSaw.real_valueX, real_valueY=currentboard.real_valueY)
        board2 = Cut(posX=currentboard.posX,posY=currentboard.posY + currentcut.valueY + CurrentSaw.valueX, mainboard=currentboard.mainboard,
                        valueX=currentcut.valueX,valueY=currentboard.valueY - currentcut.valueY - CurrentSaw.valueX,
                        real_valueX=currentcut.real_valueX, real_valueY=currentboard.real_valueY - currentcut.real_valueY - CurrentSaw.real_valueX)
    else:
        # horizontal cut
        # Create the left over boards and put them in Available boards
        inc = Incision(currentboard.posX, currentboard.posY + currentcut.valueY, currentboard.posX + currentboard.valueX, currentboard.posY + currentcut.valueY, currentboard.mainboard)
        incisions.append(copy.deepcopy(inc))
        board1 = Cut(posX=currentboard.posX,posY=currentboard.posY + currentcut.valueY + CurrentSaw.valueX, mainboard=currentboard.mainboard,
                        valueX=currentboard.valueX,valueY=currentboard.valueY - currentcut.valueY - CurrentSaw.valueX,
                        real_valueX=currentboard.real_valueX, real_valueY=currentboard.real_valueY - currentcut.real_valueY - CurrentSaw.real_valueX)
        board2 = Cut(posX=currentboard.posX + currentcut.valueX + CurrentSaw.valueX,posY=currentboard.posY, mainboard=currentboard.mainboard,
                        valueX=currentboard.valueX - currentcut.valueX - CurrentSaw.valueX,valueY=currentcut.valueY,
                        real_valueX=currentboard.real_valueX - currentcut.real_valueX - CurrentSaw.real_valueX, real_valueY=currentcut.real_valueY)
    # check if the created boards are real
    if board1.valueX > 0 and board1.valueY > 0:
        sortedavailableboards.append(board1)
    if board2.valueX > 0 and board2.valueY > 0:
        sortedavailableboards.append(board2)

def rotation_setup(currentcut, currentboard, sortedcutslist):
    rotate = False
    if currentcut.direction == False: 
        if (currentboard.valueX >= currentcut.valueY and currentboard.valueY >= currentcut.valueX and
            (currentboard.valueX < currentcut.valueX or currentboard.valueY < currentcut.valueY)):
            rotate = True
        # if possible to rotate
        elif (currentboard.valueX >= currentcut.valueX and currentboard.valueY >= currentcut.valueY and 
        currentboard.valueX >= currentcut.valueY and currentboard.valueY >= currentcut.valueX):
            rotate = better_to_rotate(currentcut, currentboard, sortedcutslist, CurrentSaw)
    return rotate

def better_to_cut_h(currentcut, currentboard, sortedcutslist, currentsaw):
    # create precuts (leftover boards after we make a cut), real values added for better debuging
    labels = ['precut2A','precut2B','precut1A','precut1B'] # switched so that it alligns in counter
    precut1A ,precut1B ,precut2A ,precut2B = precut_creation(labels, currentcut, currentboard, currentsaw)
    precuts_for_cutting = [precut1A, precut1B, precut2A, precut2B]
    # compare each subsequent cut to the precuts to see of it fits
    return result_calc(precuts_for_cutting, sortedcutslist)

def better_to_rotate(currentcut, currentboard, sortedcutslist, currentsaw):
    copy_currentcut = copy.deepcopy(currentcut)
    # create precuts (imaginary cuts that would be made if we cut the board in given rotation), real values added for better debuging
    # horizontal
    labels = ['precut1A','precut1B','precut1C','precut1D']
    precut1A, precut1B, precut2A, precut2B = precut_creation(labels, copy_currentcut, currentboard, currentsaw)
    
    copy_currentcut.valueX, copy_currentcut.valueY = value_switch(copy_currentcut.valueX, copy_currentcut.valueY)
    copy_currentcut.real_valueX, copy_currentcut.real_valueY = value_switch(copy_currentcut.real_valueX, copy_currentcut.real_valueY)
    # vertical
    labels = ['precut2A','precut2B','precut2C','precut2D']
    precut3A, precut3B, precut4A, precut4B = precut_creation(labels, copy_currentcut, currentboard, currentsaw)
    precuts_for_rotation = [precut1A, precut1B, precut2A, precut2B, precut3A, precut3B, precut4A, precut4B]
    # compare each subsequent cut to the precuts to see of it fits
    return result_calc(precuts_for_rotation, sortedcutslist)

def precut_creation(labels, currentcut, currentboard, currentsaw):
    precut1A = Cut(count=0, label=labels[0], valueX=currentboard.valueX - currentcut.valueX - currentsaw.valueX , valueY=currentboard.valueY,
                  real_valueX=currentboard.real_valueX - currentcut.real_valueX - currentsaw.real_valueX, real_valueY=currentboard.real_valueY)
    precut1B = Cut(count=0, label=labels[1], valueX=currentcut.valueX, valueY=currentboard.valueY - currentcut.valueY - currentsaw.valueX,
                  real_valueX=currentcut.valueX, real_valueY=currentboard.real_valueY - currentcut.real_valueY - currentsaw.real_valueX)
    precut2A = Cut(count=0, label=labels[2], valueX=currentboard.valueX, valueY=currentboard.valueY - currentcut.valueY - currentsaw.valueX,
                  real_valueX=currentboard.real_valueX, real_valueY=currentboard.real_valueY - currentcut.real_valueY - currentsaw.real_valueX)
    precut2B = Cut(count=0, label=labels[3], valueX=currentboard.valueX - currentcut.valueX - currentsaw.valueX, valueY=currentcut.valueY,
                  real_valueX=currentboard.real_valueX - currentcut.real_valueX - currentsaw.real_valueX, real_valueY=currentcut.real_valueY)
    return precut1A, precut1B, precut2A, precut2B

def result_calc(precuts, sortedcutslist):
    copiedsortedcutslist = copy.deepcopy(sortedcutslist)
    #compare each with each and keep count of what fits
    for cut in copiedsortedcutslist:
        for precut in precuts:
            if (cut.valueX <= precut.valueX and cut.valueY <= precut.valueY or
                cut.valueX <= precut.valueY and cut.valueY <= precut.valueX):
                precut.count += 1
    count1, count2 = count_count(precuts)
    # if the logic above didnt give result - happens if there is not many following cuts to consider,
    # or if the precuts are similar
    # in that case we should make the cut that leaves the biggest piece
    if count1 == count2:
        # what if 2 precuts are the same therefore this do nothing - both options are fine?
        precutwithbiggestpiece = max(precuts, key=lambda precut: precut.valueX * precut.valueY)
        for precut in precuts:
            if precut.label == precutwithbiggestpiece.label:
                precut.count += 1
    # recount the results
    count1, count2 = count_count(precuts)
    if count2 > count1:
        return True
    else: return False

def count_count(precuts):
    count1, count2 = 0, 0
    for precut in precuts:
        if "precut1" in precut.label:
            count1 += precut.count
        elif "precut2" in precut.label:
            count2 += precut.count
    return count1, count2

def list_setup(cutslist, boardslist, div):
    for each in cutslist:
        each.valueX = each.real_valueX / div
        each.valueY = each.real_valueY / div
        if each.direction == False:
            if each.valueX < each.valueY:
                each.valueX, each.valueY = value_switch(each.valueX, each.valueY)
    # copy all the way here so that it gets the values but isnt changed after
    sorted_cutslist = sorted(copy.deepcopy(cutslist), key=lambda obj: obj.valueX * obj.valueY)
    # TODO: necessary since its only 1 board?
    sorted_availableboards = sorted(boardslist, key=lambda obj: obj.valueX * obj.valueY, reverse=True)
    return sorted_cutslist, sorted_availableboards

def create_available_boards(div, mainboardcount):
    NewCut = Cut(real_valueX=MainBoard.real_valueX, real_valueY=MainBoard.real_valueY, valueX=(MainBoard.real_valueX - pdf.Crop) / div,
                  valueY=(MainBoard.real_valueY - pdf.Crop) / div, mainboard=mainboardcount)
    return NewCut

def find_divider():
    Divider = 1
    MainBoardWidth = MainBoard.real_valueX
    MainBoardHeight = MainBoard.real_valueY
    RecAvailableWidth = pdf.AvailableWidth / ProjectProperties['Coeficient'] # how much smaller do i want it
    RecAvailableHeight = pdf.AvailableHeight / ProjectProperties['Coeficient'] / 1.5 # the vertical boards seem to be too big
    while MainBoardWidth > RecAvailableWidth and MainBoardHeight > RecAvailableHeight:
        Divider += 0.2
        if MainBoardWidth / Divider <= RecAvailableWidth and MainBoardHeight / Divider <= RecAvailableHeight:
            return Divider

def value_switch(n1, n2):
    return n2, n1

Divider, MadeBoards, Incisions, SortedAvailableBoards = Logic()