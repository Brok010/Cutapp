class Saw:
    def __init__(self, label='Saw', valueX=0, real_valueX = 3, notes='No notes', generate = False):
        self.label = label
        self.valueX = valueX
        self.real_valueX = real_valueX
        self.notes = notes
        self.generate = generate
    
    def __str__(self):
        return (f'SawClass(Label= {self.label}, valueX= {self.valueX}, real_valueX= {self.real_valueX}, '
                f'notes= {self.notes},generate= {self.generate})')