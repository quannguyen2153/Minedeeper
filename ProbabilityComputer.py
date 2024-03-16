import copy

def countEdge(board, size):
    numRows = size[0]
    numColumns = size[1]
    
    for i in range(numRows):
        for j in range(numColumns):
            if board[i][j].type == 9:
                board[i][j].edge = False
                continue
            
            count = 0
            if board[i][j].open:
                board[i][j].edge = False
                # Left
                if j > 0:
                    if not board[i][j-1].open:
                        board[i][j-1].edge = True
                        count += 1
                # Upper Left
                if i > 0 and j > 0:
                    if not board[i-1][j-1].open:
                        board[i-1][j-1].edge = True
                        count += 1
                # Up
                if i > 0:
                    if not board[i-1][j].open:
                        board[i-1][j].edge = True
                        count += 1
                # Upper Right
                if i > 0 and j < (numColumns-1):
                    if not board[i-1][j+1].open:
                        board[i-1][j+1].edge = True
                        count += 1
                # Right
                if j < (numColumns-1):
                    if not board[i][j+1].open:
                        board[i][j+1].edge = True
                        count += 1
                # Bottom Right
                if i < (numRows-1) and j < (numColumns-1):
                    if not board[i+1][j+1].open:
                        board[i+1][j+1].edge = True
                        count += 1
                # Bottom
                if i < (numRows-1):
                    if not board[i+1][j].open:
                        board[i+1][j].edge = True
                        count += 1
                # Bottom Left
                if i < (numRows-1) and j > 0:
                    if not board[i+1][j-1].open:
                        board[i+1][j-1].edge = True
                        count += 1
                        
            board[i][j].edgeCount = count
            
def probabilityZeroCount(board, size, i, j):
    numRows = size[0]
    numColumns = size[1]
    
    count = 0
    # Left
    if j > 0:
        if board[i][j-1].probability == 0:
            count += 1
    # Upper Left
    if i > 0 and j > 0:
        if board[i-1][j-1].probability == 0:
            count += 1
    # Up
    if i > 0:
        if board[i-1][j].probability == 0:
            count += 1
    # Upper Right
    if i > 0 and j < (numColumns-1):
        if board[i-1][j+1].probability == 0:
            count += 1
    # Right
    if j < (numColumns-1):
        if board[i][j+1].probability == 0:
            count += 1
    # Bottom Right
    if i < (numRows-1) and j < (numColumns-1):
        if board[i+1][j+1].probability == 0:
            count += 1
    # Bottom
    if i < (numRows-1):
        if board[i+1][j].probability == 0:
            count += 1
    # Bottom Left
    if i < (numRows-1) and j > 0:
        if board[i+1][j-1].probability == 0:
            count += 1
    return count

# Label cell must be mine by basic logic rules
def ruleOne(board, size, hundredCount):
    ret = False
    hundredCountUpdate = hundredCount
    
    numRows = size[0]
    numColumns = size[1]
    
    for i in range(numRows):
        for j in range(numColumns):
            if board[i][j].edgeCount > 0 and board[i][j].type == board[i][j].edgeCount - probabilityZeroCount(board=board, size=size, i=i, j=j):
                # Left
                if j > 0:
                    if board[i][j-1].edge and board[i][j-1].probability < 0:
                        board[i][j-1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Upper Left
                if i > 0 and j > 0:
                    if board[i-1][j-1].edge and board[i-1][j-1].probability < 0:
                        board[i-1][j-1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Up
                if i > 0:
                    if board[i-1][j].edge and board[i-1][j].probability < 0:
                        board[i-1][j].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Upper Right
                if i > 0 and j < (numColumns-1):
                    if board[i-1][j+1].edge and board[i-1][j+1].probability < 0:
                        board[i-1][j+1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Right
                if j < (numColumns-1):
                    if board[i][j+1].edge and board[i][j+1].probability < 0:
                        board[i][j+1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Bottom Right
                if i < (numRows-1) and j < (numColumns-1):
                    if board[i+1][j+1].edge and board[i+1][j+1].probability < 0:
                        board[i+1][j+1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Bottom
                if i < (numRows-1):
                    if board[i+1][j].edge and board[i+1][j].probability < 0:
                        board[i+1][j].probability = 100
                        hundredCountUpdate += 1
                        ret = True
                # Bottom Left
                if i < (numRows-1) and j > 0:
                    if board[i+1][j-1].edge and board[i+1][j-1].probability < 0:
                        board[i+1][j-1].probability = 100
                        hundredCountUpdate += 1
                        ret = True
    
    return ret, hundredCountUpdate

def probabilityHundredCount(board, size, i, j):
    numRows = size[0]
    numColumns = size[1]
    
    count = 0
    
    # Left
    if j > 0:
        if board[i][j-1].probability == 100:
            count += 1
    # Upper Left
    if i > 0 and j > 0:
        if board[i-1][j-1].probability == 100:
            count += 1
    # Up
    if i > 0:
        if board[i-1][j].probability == 100:
            count += 1
    # Upper Right
    if i > 0 and j < (numColumns-1):
        if board[i-1][j+1].probability == 100:
            count += 1
    # Right
    if j < (numColumns-1):
        if board[i][j+1].probability == 100:
            count += 1
    # Bottom Right
    if i < (numRows-1) and j < (numColumns-1):
        if board[i+1][j+1].probability == 100:
            count += 1
    # Bottom
    if i < (numRows-1):
        if board[i+1][j].probability == 100:
            count += 1
    # Bottom Left
    if i < (numRows-1) and j > 0:
        if board[i+1][j-1].probability == 100:
            count += 1
    return count

def ruleTwo(board, size):
    ret = False
    
    numRows = size[0]
    numColumns = size[1]
    
    for i in range(numRows):
        for j in range(numColumns):
            if board[i][j].edgeCount > 0 and board[i][j].type == probabilityHundredCount(board=board, size=size, i=i, j=j):
                # Left
                if j > 0:
                    if board[i][j-1].edge and board[i][j-1].probability < 0:
                        board[i][j-1].probability = 0
                        ret = True
                # Upper Left
                if i > 0 and j > 0:
                    if board[i-1][j-1].edge and board[i-1][j-1].probability < 0:
                        board[i-1][j-1].probability = 0
                        ret = True
                # Up
                if i > 0:
                    if board[i-1][j].edge and board[i-1][j].probability < 0:
                        board[i-1][j].probability = 0
                        ret = True
                # Upper Right
                if i > 0 and j < (numColumns-1):
                    if board[i-1][j+1].edge and board[i-1][j+1].probability < 0:
                        board[i-1][j+1].probability = 0
                        ret = True
                # Right
                if j < (numColumns-1):
                    if board[i][j+1].edge and board[i][j+1].probability < 0:
                        board[i][j+1].probability = 0
                        ret = True
                # Bottom Right
                if i < (numRows-1) and j < (numColumns-1):
                    if board[i+1][j+1].edge and board[i+1][j+1].probability < 0:
                        board[i+1][j+1].probability = 0
                        ret = True
                # Bottom
                if i < (numRows-1):
                    if board[i+1][j].edge and board[i+1][j].probability < 0:
                        board[i+1][j].probability = 0
                        ret = True
                # Bottom Left
                if i < (numRows-1) and j > 0:
                    if board[i+1][j-1].edge and board[i+1][j-1].probability < 0:
                        board[i+1][j-1].probability = 0
                        ret = True
    return ret

# Count how many cells that are open are around a cell
def openCount(board, size, i, j):
    numRows = size[0]
    numColumns = size[1]
    
    count = 0
    
    # Left
    if j > 0:
        if board[i][j-1].open:
            count += 1
    # Upper Left
    if i > 0 and j > 0:
        if board[i-1][j-1].open:
            count += 1
    # Up
    if i > 0:
        if board[i-1][j].open:
            count += 1
    # Upper Right
    if i > 0 and j < (numColumns-1):
        if board[i-1][j+1].open:
            count += 1
    # Right
    if j < (numColumns-1):
        if board[i][j+1].open:
            count += 1
    # Bottom Right
    if i < (numRows-1) and j < (numColumns-1):
        if board[i+1][j+1].open:
            count += 1
    # Bottom
    if i < (numRows-1):
        if board[i+1][j].open:
            count += 1
    # Bottom Left
    if i < (numRows-1) and j > 0:
        if board[i+1][j-1].open:
            count += 1
    return count

# Label isolated cells that have independently determined probabilities
def ruleThree(board, size):
    numRows = size[0]
    numColumns = size[1]
    
    mineFound = 0
    
    for i in range(numRows):
        for j in range(numColumns):
            if board[i][j].edgeCount > 2:
                count = 0
                # Left
                if j > 0:
                    if board[i][j-1].edge and openCount(board, size, i, j-1) == 1:
                        count += 1
                # Upper Left
                if i > 0 and j > 0:
                    if board[i-1][j-1].edge and openCount(board, size, i-1, j-1) == 1:
                        count += 1
                # Up
                if i > 0:
                    if board[i-1][j].edge and openCount(board, size, i-1, j) == 1:
                        count += 1
                # Upper Right
                if i > 0 and j < (numColumns-1):
                    if board[i-1][j+1].edge and openCount(board, size, i-1, j+1) == 1:
                        count += 1
                # Right
                if j < (numColumns-1):
                    if board[i][j+1].edge and openCount(board, size, i, j+1) == 1:
                        count += 1
                # Bottom Right
                if i < (numRows-1) and j < (numColumns-1):
                    if board[i+1][j+1].edge and openCount(board, size, i+1, j+1) == 1:
                        count += 1
                # Bottom
                if i < (numRows-1):
                    if board[i+1][j].edge and openCount(board, size, i+1, j) == 1:
                        count += 1
                # Bottom Left
                if i < (numRows-1) and j > 0:
                    if board[i+1][j-1].edge and openCount(board, size, i+1, j-1) == 1:
                        count += 1
                        
                if count == board[i][j].edgeCount:
                    mineFound += board[i][j].type
                    
                    probability = round(board[i][j].type / board[i][j].edgeCount * 100)
                    # Left
                    if j > 0:
                        board[i][j-1].probability = probability
                    # Upper Left
                    if i > 0 and j > 0:
                        board[i-1][j-1].probability = probability
                    # Up
                    if i > 0:
                        board[i-1][j].probability = probability
                    # Upper Right
                    if i > 0 and j < (numColumns-1):
                        board[i-1][j+1].probability = probability
                    # Right
                    if j < (numColumns-1):
                        board[i][j+1].probability = probability
                    # Bottom Right
                    if i < (numRows-1) and j < (numColumns-1):
                        board[i+1][j+1].probability = probability
                    # Bottom
                    if i < (numRows-1):
                        board[i+1][j].probability = probability
                    # Bottom Left
                    if i < (numRows-1) and j > 0:
                        board[i+1][j-1].probability = probability
                        
    return mineFound
                        
# Find the next "edge" cell with an assigned logical probability starting from the given index
def findNextEdge(board, size, x, y):
    numRows = size[0]
    numColumns = size[1]
    
    for i in range(x, numRows):
        for j in range(y, numColumns):
            if board[i][j].edge and board[i][j].probability < 0:
                return [i,j]
        y = 0
    return [-1, -1]

# Count how many theoretical mines are placed around a cell when generating arrangements
def mineCount(grid, i, j):
    count = 0
    
    for k in range(len(grid)):
        if grid[k].r >= i-1 and grid[k].r <= i+1 and grid[k].c >= j-1 and grid[k].c <= j+1:
            if grid[k].mine == True:
                count += 1
                
    return count

# Determine if a cell can be a mine by looking at open nearby numbers
def canBeMine(board, size, grid, i, j):
    numRows = size[0]
    numColumns = size[1]
    
    # Left
    if j > 0:
        if board[i][j-1].type == 9:
            pass
        elif board[i][j-1].open and board[i][j-1].type <= mineCount(grid, i, j-1) + probabilityHundredCount(board, size, i, j-1):
            return False
    # Upper Left
    if i > 0 and j > 0:
        if board[i-1][j-1].type == 9:
            pass
        elif board[i-1][j-1].open and board[i-1][j-1].type <= mineCount(grid, i-1, j-1) + probabilityHundredCount(board, size, i-1, j-1):
            return False
    # Up
    if i > 0:
        if board[i-1][j].type == 9:
            pass        
        elif board[i-1][j].open and board[i-1][j].type <= mineCount(grid, i-1, j) + probabilityHundredCount(board, size, i-1, j):
            return False
    # Upper Right
    if i > 0 and j < (numColumns-1):
        if board[i-1][j+1].type == 9:
            pass
        elif board[i-1][j+1].open and board[i-1][j+1].type <= mineCount(grid, i-1, j+1) + probabilityHundredCount(board, size, i-1, j+1):
            return False
    # Right
    if j < (numColumns-1):
        if board[i][j+1].type == 9:
            pass
        elif board[i][j+1].open and board[i][j+1].type <= mineCount(grid, i, j+1) + probabilityHundredCount(board, size, i, j+1):
            return False
    # Bottom Right
    if i < (numRows-1) and j < (numColumns-1):
        if board[i+1][j+1].type == 9:
            pass
        elif board[i+1][j+1].open and board[i+1][j+1].type <= mineCount(grid, i+1, j+1) + probabilityHundredCount(board, size, i+1, j+1):
            return False
    # Bottom
    if i < (numRows-1):
        if board[i+1][j].type == 9:
            pass
        elif board[i+1][j].open and board[i+1][j].type <= mineCount(grid, i+1, j) + probabilityHundredCount(board, size, i+1, j):
            return False
    # Bottom Left
    if i < (numRows-1) and j > 0:
        if board[i+1][j-1].type == 9:
            pass
        elif board[i+1][j-1].open and board[i+1][j-1].type <= mineCount(grid, i+1, j-1) + probabilityHundredCount(board, size, i+1, j-1):
            return False
    return True

# Count how many theoretical nonmines are placed around a cell when generating arrangements
def noMineCount(grid, i, j):
    count = 0
    
    for k in range(len(grid)):
        if grid[k].r >= i-1 and grid[k].r <= i+1 and grid[k].c >= j-1 and grid[k].c <= j+1:
            if (grid[k].mine == False):
                count += 1
                
    return count

# Determine if a cell can be not a mine by looking at open nearby numbers
def canNotBeMine(board, size, grid, i, j):
    numRows = size[0]
    numColumns = size[1]    
    
    # Left
    if j > 0:
        if board[i][j-1].type == 9:
            pass
        elif board[i][j-1].open and board[i][j-1].type >= board[i][j-1].edgeCount - noMineCount(grid, i, j-1) - probabilityZeroCount(board, size, i, j-1):
            return False
    # Upper Left
    if i > 0 and j > 0:
        if board[i-1][j-1].type == 9:
            pass
        elif board[i-1][j-1].open and board[i-1][j-1].type >= board[i-1][j-1].edgeCount - noMineCount(grid, i-1, j-1) - probabilityZeroCount(board, size, i-1, j-1):
            return False
    # Up
    if i > 0:
        if board[i-1][j].type == 9:
            pass
        elif board[i-1][j].open and board[i-1][j].type >= board[i-1][j].edgeCount - noMineCount(grid, i-1, j) - probabilityZeroCount(board, size, i-1, j):
            return False
    # Upper Right
    if i > 0 and j < (numColumns-1):
        if board[i-1][j+1].type == 9:
            pass
        elif board[i-1][j+1].open and board[i-1][j+1].type >= board[i-1][j+1].edgeCount - noMineCount(grid, i-1, j+1) - probabilityZeroCount(board, size, i-1, j+1):
            return False
    # Right
    if j < (numColumns-1):
        if board[i][j+1].type == 9:
            pass
        elif board[i][j+1].open and board[i][j+1].type >= board[i][j+1].edgeCount - noMineCount(grid, i, j+1) - probabilityZeroCount(board, size, i, j+1):
            return False
    # Bottom Right
    if i < (numRows-1) and j < (numColumns-1):
        if board[i+1][j+1].type == 9:
            pass
        elif board[i+1][j+1].open and board[i+1][j+1].type >= board[i+1][j+1].edgeCount - noMineCount(grid, i+1, j+1) - probabilityZeroCount(board, size, i+1, j+1):
            return False
    # Bottom
    if i < (numRows-1):
        if board[i+1][j].type == 9:
            pass
        elif board[i+1][j].open and board[i+1][j].type >= board[i+1][j].edgeCount - noMineCount(grid, i+1, j) - probabilityZeroCount(board, size, i+1, j):
            return False
    # Bottom Left
    if i < (numRows-1) and j > 0:
        if board[i+1][j-1].type == 9:
            pass
        elif board[i+1][j-1].open and board[i+1][j-1].type >= board[i+1][j-1].edgeCount - noMineCount(grid, i+1, j-1) - probabilityZeroCount(board, size, i+1, j-1):
            return False
    return True

# Recursively generate all possible mine arrangements for open edges
def generateArrangements(board, size, grid, index, edgeArr):
    i = grid[index].r
    j = grid[index].c
    
    if canBeMine(board, size, grid, i, j):
        patternYes = copy.deepcopy(grid)
        patternYes[index].mine = True
        if index < (len(grid) - 1):
            generateArrangements(board, size, patternYes, index+1, edgeArr)
        else:
            edgeArr.append(patternYes)
    if canNotBeMine(board, size, grid, i, j):
        patternNo = copy.deepcopy(grid)
        patternNo[index].mine = False
        if index < (len(grid) - 1):
            generateArrangements(board, size, patternNo, index+1, edgeArr)
        else:
            edgeArr.append(patternNo)
            
# Count how many cells are neither open nor bordering open cells
def nonEdgeCount(board):
    count = 0
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].open == False and board[i][j].edge == False:
                count += 1
                
    return count

# Calculate combinations math
def combinations(n, r):
    # Function used for combinations calculation
    def productRange(a, b):
        prd = a
        i = a
    
        while i < b:
            prd*=i
            i += 1
            
        return prd
    
    if n == r or r == 0:
      return 1
    else:
        if r < n - r:
            r = n - r
        return productRange(r + 1, n) / productRange(1, n - r)
            
# Calculate probabilities from given mine arrangements
def probabilityCalculation(edgeArr, board, size, numMines, hundredCount, mineFound, allProbability):
    # Store where mines are placed in each arrangement and find the total number of arrangements
    arrCount = 0
    nonEdge = nonEdgeCount(board)
    
    for k in range(len(edgeArr)):
        minesPlaced = 0
        for i in range(len(edgeArr[k])):
            if edgeArr[k][i].mine == True:
                minesPlaced += 1
                
        remainingMines = numMines - minesPlaced - hundredCount - mineFound
        if remainingMines >= 0 and remainingMines <= nonEdge:
            nonEdgeCombinations = combinations(nonEdge, remainingMines)
            for i in range(len(edgeArr[k])):
                if edgeArr[k][i].mine == True:
                    board[edgeArr[k][i].r][edgeArr[k][i].c].mineArr += nonEdgeCombinations
                    
            arrCount += nonEdgeCombinations
            
            for i in range(size[0]):
                for j in range(size[1]):
                    if board[i][j].open == False and board[i][j].edge == False:
                        board[i][j].mineArr += remainingMines / nonEdge * nonEdgeCombinations

    # Calculate probability of each cell by dividing the number of arrangements with mines in each cell by total arrangements
    for i in range(size[0]):
        for j in range(size[1]):
            if board[i][j].edge == True and board[i][j].probability < 0:
                edgeProbability = round(board[i][j].mineArr / arrCount * 100)
                if allProbability == False and (edgeProbability == 100 or edgeProbability == 0):
                    board[i][j].probability = edgeProbability
                if allProbability == True:
                    board[i][j].probability = edgeProbability
                    
            if board[i][j].open == False and board[i][j].edge == False and board[i][j].probability < 0:
                nonEdgeProbability = round(board[i][j].mineArr / arrCount * 100)
                if allProbability == False and (nonEdgeProbability == 100 or nonEdgeProbability == 0):
                    board[i][j].probability = nonEdgeProbability
                if allProbability == True:
                    board[i][j].probability = nonEdgeProbability

def computeProbability(board, size, total_mines, guessLocation, isAllProbability=True):
    yield "Analyzing"
    
    if not guessLocation in computedBoards:
        # Reset old probability values
        for i in range(size[0]):
            for j in range(size[1]):
                board[i][j].mineArr = 0
                board[i][j].probability = -1
                board[i][j].edge = False
                board[i][j].edgeCount = 0
        
        numColumns = size[1]
        
        hundredCount = 0
        arrGrid = []
        edgeArr = []
        
        countEdge(board, size)
        
        # Apply basic rule    
        yield "Applying Basic Rules"
        
        ret1 = True
        ret2 = True
        while ret1 or ret2:
            ret1, hundredCount = ruleOne(board, size, hundredCount)
            ret2 = ruleTwo(board, size)
        mineFound = ruleThree(board, size)
        
        # Calculate arrangements and probabilities
        yield "Generating Arrangements"
        
        class HypotheticalCell():
            def __init__(self, mine, r, c) -> None:
                self.mine = mine
                self.r = r
                self.c = c
        
        index = findNextEdge(board, size, 0, 0)
        i = index[0]
        j = index[1]
        
        while i > -1:
            arrGrid.append(HypotheticalCell(mine=None, r=i, c=j))
            if j == numColumns - 1:
                index = findNextEdge(board, size, i+1, 0)
                i = index[0]
                j = index[1]
            else:
                index = findNextEdge(board, size, i, j+1)
                i = index[0]
                j = index[1]
                
        if len(arrGrid) > 0:
            generateArrangements(board, size, arrGrid, 0, edgeArr)
            
            yield "Calculating Probabilities"
            probabilityCalculation(edgeArr, board, size, total_mines, hundredCount, mineFound, isAllProbability)
        else:
            yield "Calculating Probabilities"
            
            nonEdge = nonEdgeCount(board)
            remainingMines = total_mines - hundredCount - mineFound
            for i in range(size[0]):
                for j in range(size[1]):
                    if board[i][j].open == False and board[i][j].edge == False:
                        board[i][j].probability = round(remainingMines / nonEdge * 100)
                        
        probabilityBoard = []
        for row in board:
            probabilityBoard.append([cell.probability for cell in row])                        
        computedBoards[guessLocation] = probabilityBoard
        
        if guessLocation is None:
            for i in range(size[0]):
                for j in range(size[1]):
                    if board[i][j].probability == 100:
                        board[i][j].guessing = False
        
    else:
        countEdge(board, size)
        for i in range(size[0]):
            for j in range(size[1]):
                board[i][j].probability = computedBoards[guessLocation][i][j]
                    
    yield "Analyzed"

def countDiscoveredMines(board):
    count = 0
    for row in board:
        for cell in row:
            if cell.probability == 100:
                count += 1
    return count

def countUnopenedSafeCells(board):
    count = 0
    for row in board:
        for cell in row:
            if cell.probability == 0:
                count += 1
    return count

def clearComputedBoards():
    computedBoards.clear()
    
def isComputed(guessLocation):
    if guessLocation in computedBoards:
        return True
    return False

computedBoards = {}