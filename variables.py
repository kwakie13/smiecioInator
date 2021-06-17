WINDOW_TITLE = "smiecioInator"

TILE_SIZE = 64
WIDTH = 768
HEIGHT = 768
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GREY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLUE = (0, 102, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MEDIUM_GREY = (70, 70, 70)

BG_COLOR = MEDIUM_GREY

TYPES_DICT = {0: "metal", 1: "plastic", 2: "paper", 3: "glass"}
TYPES_COLOR = {"metal": GREY, "plastic": YELLOW, "paper": BLUE, "glass": GREEN}
TYPES_PICS = {"metal": './Assets/trash_metal.png', "plastic": './Assets/trash_plastic.png',
              "paper": './Assets/trash_paper.png', "glass": './Assets/trash_glass.png'}
TYPES_PICS_SETS = {"metal": './Assets/test_set/metal', "plastic": './Assets/test_set/plastic',
                   "paper": './Assets/test_set/paper', "glass": './Assets/test_set/glass'}

TRUCK_PICS = {0: './Assets/truck_0.png', 1: './Assets/truck_1.png', 2: './Assets/truck_2.png',
              3: './Assets/truck_3.png'}

HOUSE_PICS = {0: './Assets/house_0.png', 1: './Assets/house_1.png', 2: './Assets/house_2.png'}

REGULAR_COST = 1
HOLE_COST = 25

TIME_BETWEEN_AUTO_MOVES = 0.1
