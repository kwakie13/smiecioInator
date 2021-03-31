class House:    #domostwa, z których będziemy odbierali śmieci
    def __init__(self, x, y, state, trash, image):
        self.position = (x, y)
        self.state = False
        self.trash = trash
        self.image = image
