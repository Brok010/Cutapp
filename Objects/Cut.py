class Cut:
    def __init__(self, label='Cut', valueX=0, valueY=0, generate = False, posX=0, posY=0,
                  mainboard=1, real_valueX = 0, real_valueY = 0, notes = 'No notes', count = 1, direction = False):
        self.label = label
        self.real_valueX = real_valueX
        self.real_valueY = real_valueY 
        self.generate = generate
        self.posX = posX
        self.posY = posY
        self.mainboard = mainboard
        self.valueX = valueX
        self.valueY = valueY
        self.notes = notes
        self.count = count
        self.direction = direction

    def __str__(self):
        return (f'CutClass(Label= {self.label}, real_valueX= {self.real_valueX}, real_valueY= {self.real_valueY}, '
                f'generate= {self.generate},posX= {self.posX}, posY= {self.posY}, mainboard= {self.mainboard}, '
                f'valueX = {self.valueX}, valueY= {self.valueY}, notes= {self.notes}, count= {self.count}, '
                f'direction= {self.direction})')