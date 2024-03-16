import cv2
import numpy as np
import copy

class MSCell():
    def __init__(self, cell):
        self.pxLocation = cell.location
        
        self.type = cell.type
        self.probability = -1
        
        self.open = self.type >= 0
        
        self.edge = False
        self.edgeCount = 0
        
        self.mineArr = 0
        
        self.guessing = True

class MSBoard():
    def __init__(self, board_image, remaining_mines, num_flag, board, time, board_locations) -> None:
        self.image = board_image
        self.total_mines = remaining_mines + num_flag
        
        self.board = []
        for row in board:
            self.board.append([MSCell(cell=cell) for cell in row])
        
        self.size = (len(self.board), len(self.board[0]))
        
        self.remaining_mines = remaining_mines
        self.total_flags = num_flag
        
        self.time = time
        self.cells_location = board_locations
    
    def copyImage(self):
        return copy.deepcopy(self.image)

def loadAssets(assets_path="assets/minesweeper_online/png/"):
    # Load the haystack and needle images
    closed_cell_image = cv2.imread(assets_path + 'closed.png')
    flag_image = cv2.imread(assets_path + 'flag.png')
    flag_wrong_image = cv2.imread(assets_path + 'mine_wrong.png')
    mine_image = cv2.imread(assets_path + 'mine.png')
    mine_exploded_image = cv2.imread(assets_path + 'mine_red.png')
    face_unpressed_image = cv2.imread(assets_path + 'face_unpressed.png')
    face_lose_image = cv2.imread(assets_path + 'face_lose.png')
    
    opened_cell_images = []
    for i in range(9):
        opened_cell_images.append(cv2.imread(assets_path + 'type' + str(i) + '.png'))
        
    number_images = []
    for i in range(10):
        number_images.append(cv2.imread(assets_path + 'd' + str(i) + '.png'))
        
    corner_up_left_image = cv2.imread(assets_path + "corner_up_left_2x.png")
    corner_bottom_right_image = cv2.imread(assets_path + "corner_bottom_right_2x.png")
        
    assets = {
        "CORNERS": [corner_up_left_image, corner_bottom_right_image],
        "CLOSED_CELL": closed_cell_image,
        "OPENED_CELLS": opened_cell_images,
        "FLAG": flag_image,
        "FLAG_WRONG": flag_wrong_image,
        "MINE_IMAGE": mine_image,
        "MINE_EXPLODED": mine_exploded_image,
        "FACE_UNPRESSED": face_unpressed_image,
        "FACE_LOSE": face_lose_image,
        "NUMBERS": number_images
    }
    
    return assets

def getCellsLocation(board_image, cell_image, cell_height, cell_width, scale, threshold, method=cv2.TM_CCOEFF_NORMED):
    # Perform template matching
    resized_cell = cv2.resize(cell_image, None, fx=scale, fy=scale)
    result = cv2.matchTemplate(board_image, resized_cell, method)
    locations = np.where(result >= threshold) # Threshold value to filter matches

    cells = []
    for loc in zip(*locations[::-1]):
        cell_border = [int(loc[0]), int(loc[1]), cell_width, cell_height]
        cells.append(cell_border)
        cells.append(cell_border)
    cells, weights = cv2.groupRectangles(cells, groupThreshold=1, eps=0.3)
    
    return cells

def cropBoardImage(board_image, corner_images, scale=0.9):
    corner_height, corner_width = [int(value * scale) for value in corner_images[0].shape[:2]]
    
    corner_up_left = getCellsLocation(board_image=board_image, cell_image=corner_images[0],
                                  cell_height=corner_height, cell_width=corner_width, scale=scale, threshold=0.94)
    corner_bottom_right = getCellsLocation(board_image=board_image, cell_image=corner_images[1],
                                  cell_height=corner_height, cell_width=corner_width, scale=scale, threshold=0.94)
    
    crop_image = board_image[corner_up_left[0][1]:corner_bottom_right[0][1]+corner_height, corner_up_left[0][0]:corner_bottom_right[0][0]+corner_width]
    
    return crop_image

def getBoardData(board_image, scale=0.3):
    if not hasattr(getBoardData, "assets"):
        getBoardData.assets = loadAssets(assets_path="assets/minesweeper_online/png/")
    
    try:
        board_image = cropBoardImage(board_image=board_image, corner_images=getBoardData.assets["CORNERS"])
    except:
        pass

    # Get the dimensions of the cell image
    cell_height, cell_width = [int(value * scale) for value in getBoardData.assets["CLOSED_CELL"].shape[:2]]
    
    closed_cells = getCellsLocation(board_image=board_image, cell_image=getBoardData.assets["CLOSED_CELL"],
                                  cell_height=cell_height, cell_width=cell_width, scale=scale, threshold=0.8)
    
    flagged_cells = getCellsLocation(board_image=board_image, cell_image=getBoardData.assets["FLAG"],
                                  cell_height=cell_height, cell_width=cell_width, scale=scale, threshold=0.8)
    
    opened_cells = []
    opened_cells.append(getCellsLocation(board_image=board_image, cell_image=getBoardData.assets["OPENED_CELLS"][0],
                                  cell_height=cell_height, cell_width=cell_width, scale=scale, threshold=0.95))
    for i in range(1, 9):
        cells = getCellsLocation(board_image=board_image, cell_image=getBoardData.assets["OPENED_CELLS"][i],
                                  cell_height=cell_height, cell_width=cell_width, scale=scale, threshold=0.7)
        opened_cells.append(cells)
        
    number_height, number_width = [int(value * 0.4) for value in getBoardData.assets["NUMBERS"][0].shape[:2]]
    numbers = []
    for i in range(10):
        cells = getCellsLocation(board_image=board_image, cell_image=getBoardData.assets["NUMBERS"][i],
                                  cell_height=number_height, cell_width=number_width,
                                  scale=0.4, threshold=0.945, method=cv2.TM_CCORR_NORMED)
        numbers.append(cells)
        
    class Cell:
        def __init__(self, location, type) -> None:
            # location = [x, y, w, h]
            self.location = location
            self.type = type        
        def isSameRow(self, other):
            if abs(self.location[1] - other.location[1]) < cell_height * 0.75:
                return True
            return False        
        def __lt__(self, other):
            if not self.isSameRow(other):
                if self.location[1] < other.location[1]:
                    return True
                return False
            else:
                if self.location[0] < other.location[0]:
                    return True
                return False
        
    cells_list = []
    cells_list.extend([Cell(cell, -1) for cell in closed_cells])
    cells_list.extend([Cell(cell, -2) for cell in flagged_cells])
    for i, opened_cell_list in enumerate(opened_cells):
        cells_list.extend([Cell(cell, i) for cell in opened_cell_list])
        
    cells_list.sort()
    
    board = []
    board.append([cells_list[0]])
    
    for i in range(1, len(cells_list)):
        if board[-1][-1].isSameRow(cells_list[i]):
            board[-1].append(cells_list[i])
        else:
            board.append([cells_list[i]])
            
    digits = []
    for i, number_list in enumerate(numbers):
        for number in number_list:
            digits.append(Cell(number, i))
    digits.sort()
    
    remaining_mines = int("".join([str(digit.type) for digit in digits[:3]]))
    try:
        time = int("".join([str(digit.type) for digit in digits[3:]]))
    except:
        time = None
    
    board_locations = {
        "CLOSED_CELL": closed_cells,
        "OPENED_CELLS": opened_cells,
        "FLAG": flagged_cells,
        "NUMBERS": numbers
    }
    
    return board_image, remaining_mines, len(flagged_cells), board, time, board_locations

def writeBoardData(remaining_mines, num_flag, board, filepath):
    with open(filepath, "w") as f:
        f.write(str(len(board)) + ' ' + str(len(board[0])) + ' ' + str(remaining_mines) + ' ' + str(num_flag) + '\n')
        for row in board:
            for cell in row:
                f.write(str(cell.type) + ' ')
            f.write('\n')

def drawCellBox(board_image, cell_location, bgrColor):
    top_left = (cell_location[0], cell_location[1])
    bottom_right = (cell_location[0] + cell_location[2], cell_location[1] + cell_location[3])
    # Draw the cell box
    cv2.rectangle(board_image, top_left, bottom_right, color=bgrColor, thickness=3)

def drawCellsBox(board_image, cells, bgrColor):
    for (x, y, w, h) in cells:
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        # Draw the cell box
        cv2.rectangle(board_image, top_left, bottom_right, color=bgrColor, thickness=2)
        
def visualizeBoard(msBoard, guessLocation, hint, detection=False):
    if detection:
        drawCellsBox(board_image=msBoard.image, cells=msBoard.cells_location["CLOSED_CELL"], bgrColor=(0, 255, 0))
        drawCellsBox(board_image=msBoard.image, cells=msBoard.cells_location["FLAG"], bgrColor=(0, 0, 255))
        for cells in msBoard.cells_location["OPENED_CELLS"]:
            drawCellsBox(board_image=msBoard.image, cells=cells, bgrColor=(255, 0, 0))
        for cells in msBoard.cells_location["NUMBERS"]:
            drawCellsBox(board_image=msBoard.image, cells=cells, bgrColor=(0, 255, 255))
    
    if hint == 1:
        hint_image = msBoard.copyImage()
        
        for i in range(msBoard.size[0]):
            for j in range(msBoard.size[1]):
                if (i, j) == guessLocation:
                    drawCellBox(board_image=hint_image, cell_location=msBoard.board[i][j].pxLocation, bgrColor=(214, 174, 79))
                elif msBoard.board[i][j].probability == -1:
                    continue
                elif msBoard.board[i][j].type == -2 and msBoard.board[i][j].probability != 100:
                    drawCellBox(board_image=hint_image, cell_location=msBoard.board[i][j].pxLocation, bgrColor=(7, 223, 247))
                elif msBoard.board[i][j].probability == 0:
                    drawCellBox(board_image=hint_image, cell_location=msBoard.board[i][j].pxLocation, bgrColor=(92, 179, 55))
                elif msBoard.board[i][j].probability == 100:
                    drawCellBox(board_image=hint_image, cell_location=msBoard.board[i][j].pxLocation, bgrColor=(31, 16, 196))
        
        cv2.imshow("Original Board With Hint", hint_image)
        cv2.waitKey()
                    
    else:        
        cv2.imshow("Original Board", msBoard.image)
        cv2.waitKey()

def getBoardInfo(input, isScreenshot):
    if isScreenshot:
        board_image = cv2.cvtColor(np.array(input), cv2.COLOR_RGB2BGR)
    else:
        board_image = cv2.imread(input)
        
    board_image, remaining_mines, num_flag, board, time, board_locations = getBoardData(board_image=board_image)
    
    num_col = len(board[0])
    for row in board:
        if num_col != len(row):
            raise Exception
    
    return MSBoard(board_image, remaining_mines, num_flag, board, time, board_locations)