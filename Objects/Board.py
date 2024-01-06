class Board:
    def __init__(self, label='Board', real_valueX=2800, real_valueY=2070, real_valueZ=18, valueX=0, valueY=0, notes='No notes', generate = False, direction = False):
        self.label = label
        self.real_valueX = real_valueX
        self.real_valueY = real_valueY
        self.real_valueZ = real_valueZ
        self.valueX = valueX
        self.valueY = valueY
        self.notes = notes
        self.generate = generate
        self.direction = direction
    
    def __str__(self):
         return (f'BoardClass(Label= {self.label}, valueX= {self.valueX}, valueY= {self.valueY}, '
                 f'valueZ= {self.valueZ},notes= {self.notes},generate= {self.generate},direction= {self.direction})')