class Waste:    #kupki na śmieci, które są na wysypisku
    def __init__(self, x, y, type, image):
        self.position = (x, y)
        self.type = type
        self.image = image
