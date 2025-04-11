import copy
import time

human_color = 'white'

board = [['white Rook','white Knight','white Bishop','white Queen','white King','white Bishop','white Knight','white Rook']]
board.append(['white Pawn']*8)
for i in range(4):
    board.append(['_']*8)
board.append(['black Pawn']*8)
board.append(['black Rook','black Knight','black Bishop','black Queen','black King','black Bishop','black Knight','black Rook'])

'''
board = [['white Rook', 'white Knight', '_', 'white Queen', 'white King', '_', 'white Knight', 'white Rook'],
['white Pawn', 'white Bishop', 'white Pawn', 'white Pawn', 'white Bishop', 'white Pawn', 'white Pawn', 'white Pawn'],
['_', 'white Pawn', '_', '_', 'white Pawn', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_', '_'],
['black Pawn', '_', 'black Knight', '_', '_', 'black Knight', '_', '_'],
['_', 'black Pawn', 'black Pawn', 'black Pawn', 'black Pawn', 'black Pawn', 'black Pawn', 'black Pawn'],
['black Rook', '_', 'black Bishop', 'black Queen', 'black King', 'black Bishop', '_', 'black Rook']]
'''
color_turn = 'black'
boards = []
computer_level = 3
check_tested = 0
legal_move_tested = 0

def is_check(board, color_turn):
    global check_tested
    check_tested+=1
    not_turn = ['white','black']
    not_turn.remove(color_turn)
    
    not_turn = ''.join(not_turn)
    king_coords = [-1,-1]
    
    # find the king on the board who may or may not be in check
    rownum = 0
    for row in board:
        
        colnum = 0
        for item in row:
            
            if item == f'{color_turn} King':
                king_coords = [rownum, colnum]
                break
            
            colnum+=1
        
        if king_coords != [-1,-1]:
            break
        else:
            rownum+=1
            
    # look at all the coordinates on the board that can potentially hit the king in a rooklike or bishoplike mannar, moving outwards and see if they are occupied by a peice that can move that way. Stop looking along a sight line if you hit a peice that cannot check, as any peice on the other side cannot check either. All knight squares are checked for knights seperately first. Pawns and enemy kings are checked seperately last because It seemed easier to do them seperately concidering I only have to check two squares for pawns and 8 for kings, and they have unique distance limitations regarding where they capture.
    
    #print(king_coords)
    #knight squares
    
    for move in [[2,1],[-2,1],[2,-1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]:
        if king_coords[0] + move[0] not in range(0,8) or king_coords[1] + move[1] not in range(0,8):
            continue
        
        if board[king_coords[0] + move[0]][king_coords[1] + move[1]] == f'{not_turn} Knight':
            return True
    
    #print('No knight')    
    #up
    if king_coords[0] < 7:
        for yform in range(king_coords[0]+2,8):
            if board[yform][king_coords[1]].startswith(str(color_turn)) or board[yform][king_coords[1]].endswith('Pawn') or board[yform][king_coords[1]].endswith('Knight') or board[yform][king_coords[1]].endswith('Bishop') or board[yform][king_coords[1]].endswith('King'):
                break
            
            else:
                if board[yform][king_coords[1]] in [f'{not_turn} Rook',f'{not_turn} Queen']:
                    return True
                
    #down
    if king_coords[0] > 0:
        for yform in range(king_coords[0]-2,-1,-1):
            if board[yform][king_coords[1]].startswith(str(color_turn)) or board[yform][king_coords[1]].endswith('Pawn') or board[yform][king_coords[1]].endswith('Knight') or board[yform][king_coords[1]].endswith('Bishop') or board[yform][king_coords[1]].endswith('King'):
                break
            
            else:
                if board[yform][king_coords[1]] in [f'{not_turn} Rook',f'{not_turn} Queen']:
                    return True
        
    #left
    if king_coords[1] > 0:
        for xform in range(king_coords[1]-2,-1,-1):
            if board[king_coords[0]][xform].startswith(str(color_turn)) or board[king_coords[0]][xform].endswith('Pawn') or board[king_coords[0]][xform].endswith('Knight') or board[king_coords[0]][xform].endswith('Bishop') or board[king_coords[0]][xform].endswith('King'):
                break
            
            else:
                if board[king_coords[0]][xform] in [f'{not_turn} Rook',f'{not_turn} Queen']:
                    return True
    
    #right
    
    if king_coords[1] < 7:
        for xform in range(king_coords[1]+2,8):
            if board[king_coords[0]][xform].startswith(str(color_turn)) or board[king_coords[0]][xform].endswith('Pawn') or board[king_coords[0]][xform].endswith('Knight') or board[king_coords[0]][xform].endswith('Bishop') or board[king_coords[0]][xform].endswith('King'):
                break
            
            else:
                if board[king_coords[0]][xform] in [f'{not_turn} Rook',f'{not_turn} Queen']:
                    return True
    
    #print('No rook')   
    
    #up left
    if king_coords[0] < 7 and king_coords[1] > 0:
        yform = king_coords[0]+2
        for xform in range(king_coords[1]-2,-1,-1):
            if yform not in range(0,8):
                break
            if board[yform][xform].startswith(str(color_turn)) or board[yform][xform].endswith('Rook') or board[yform][xform].endswith('Knight') or board[yform][xform].endswith('Pawn') or board[yform][xform].endswith('King'):
                break
            
            else:
                if board[yform][xform] in [f'{not_turn} Bishop',f'{not_turn} Queen']:
                    return True
                    
            yform+=1
                    
    
    #down left
    if king_coords[0] > 0 and king_coords[1] > 0:
        yform = king_coords[0]-2
        for xform in range(king_coords[1]-2,-1,-1):
            if yform not in range(0,8):
                break
            if board[yform][xform].startswith(str(color_turn)) or board[yform][xform].endswith('Rook') or board[yform][xform].endswith('Knight') or board[yform][xform].endswith('Pawn') or board[yform][xform].endswith('King'):
                break
            
            else:
                if board[yform][xform] in [f'{not_turn} Bishop',f'{not_turn} Queen']:
                    return True
                    
            yform-=1
            
    #up right
    if king_coords[0] < 7 and king_coords[1] < 7:
        yform = king_coords[0]+2
        for xform in range(king_coords[1]+2,8,1):
            if yform not in range(0,8):
                break
            if board[yform][xform].startswith(str(color_turn)) or board[yform][xform].endswith('Rook') or board[yform][xform].endswith('Knight') or board[yform][xform].endswith('Pawn') or board[yform][xform].endswith('King'):
                break
            
            else:
                if board[yform][xform] in [f'{not_turn} Bishop',f'{not_turn} Queen']:
                    return True
                    
            yform+=1
            
    
    #down right
    if king_coords[0] > 0 and king_coords[1] < 7:
        yform = king_coords[0]-2
        for xform in range(king_coords[1]+2,8,1):
            if yform not in range(0,8):
                break
            if board[yform][xform].startswith(str(color_turn)) or board[yform][xform].endswith('Rook') or board[yform][xform].endswith('Knight') or board[yform][xform].endswith('Pawn') or board[yform][xform].endswith('King'):
                break
            
            else:
                if board[yform][xform] in [f'{not_turn} Bishop',f'{not_turn} Queen']:
                    return True
                    
            yform-=1
          
    
    #print('No diagonal')      
    #pawn squares
    
    if color_turn == 'white':
        if king_coords[0] < 7 and king_coords[1] < 7:
            if board[king_coords[0]+1][king_coords[1]+1] == f'{not_turn} Pawn':
                return True
                
        if king_coords[0] < 7 and king_coords[1] > 0:
            if board[king_coords[0]+1][king_coords[1]-1] == f'{not_turn} Pawn':
                return True
                
    else:
        if king_coords[0] > 0 and king_coords[1] < 7:
            if board[king_coords[0]-1][king_coords[1]+1] == f'{not_turn} Pawn':
                return True
                
        if king_coords[0] > 0 and king_coords[1] > 0:
            if board[king_coords[0]-1][king_coords[1]-1] == f'{not_turn} Pawn':
                return True  
                
    #print('No pawn')                
    #check king squares
    for test in [[1,0],[0,-1],[0,1],[-1,0]]:
        if king_coords[0]+test[0] not in range(0,8) or king_coords[1]+test[1] not in range(0,8):
            continue
        
        if board[king_coords[0]+test[0]][king_coords[1]+test[1]] in [f'{not_turn} King', f'{not_turn} Rook', f'{not_turn} Queen']:
            return True

    for test in [[1,-1],[1,1],[-1,-1],[-1,1]]:
        if king_coords[0]+test[0] not in range(0,8) or king_coords[1]+test[1] not in range(0,8):
            continue
        
        if board[king_coords[0]+test[0]][king_coords[1]+test[1]] in [f'{not_turn} King', f'{not_turn} Bishop', f'{not_turn} Queen']:
            return True  
    
    #print('No King')          

def get_legal_moves(board, color_turn):
    global boards
    global legal_move_tested
    legal_move_tested+=1
    
    boards = []
    moves = []
    rownum = -1
    colum_letters = ['a','b','c','d','e','f','g','h']
    
    for row in board:
        rownum+=1
        colnum = 0
        
        for item in row:
            if item == '_' or item.startswith(color_turn) == False:
                continue
            else:
                if item.endswith('Bishop'):
                    
                    #up left
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum > 0:
                        xform -= 1
                        yform += 1

                        ycoord = yform+rownum
                        xcoord = xform+colnum
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Bishop'
                            if is_check(newboard, color_turn) == None:
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}B{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                    #up right
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum < 6:
                        xform += 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum
                        
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Bishop'
                            if is_check(newboard, color_turn) == None:
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}B{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                    
                    #down left
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum > 0:
                        xform -= 1
                        yform -= 1

                        ycoord = yform+rownum
                        xcoord = xform+colnum
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Bishop'
                            
                            if is_check(newboard, color_turn) == None:
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}B{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                    
                    #down right
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum < 6:
                        xform += 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Bishop'
                        
                            if is_check(newboard, color_turn) == None:
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}B{colum_letters[xcoord]}{ycoord+1}')
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                
                
                
                if item.endswith('Queen'):
                    
                    #left
                    xform, yform = 0,0
                    while xform+colnum > 0:
                        xform -= 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            if is_check(newboard, color_turn) == None:  
                                
                                newboard = copy.deepcopy(board)
                                newboard[rownum][colnum] = '_'
                                newboard[ycoord][xcoord] = f'{color_turn} Queen'
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                    
                    #right
                    xform, yform = 0,0
                    while xform+colnum < 6:
                        xform += 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum
                            
                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                    
                    
                    #up
                    xform, yform = 0,0
                    while yform+rownum < 6:
                        #xform -= 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                       
                       
                    #down
                    xform, yform = 0,0
                    while yform+rownum > 0:
                        #xform -= 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break 
                        
                        
                    #up left
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum > 0:
                        xform -= 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                    #up right
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum < 6:
                        xform += 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                    
                    #down left
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum > 0:
                        xform -= 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                    
                    #down right
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum < 6:
                        xform += 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Queen'
                            
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}Q{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                
                if item.endswith('Rook'):
                    
                    #left
                    xform, yform = 0,0
                    while xform+colnum > 0:
                        xform -= 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Rook'
                        
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}R{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                                
                            else:
                                break
                        
                    #right
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum < 6:
                        xform += 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Rook'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}R{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                    
                    
                    #up
                    xform, yform = 0,0
                    while yform+rownum < 6:
                        #xform -= 1
                        yform += 1
                        ycoord = yform+rownum
                        xcoord = xform+colnum
                        
                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Rook'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}R{colum_letters[xcoord]}{ycoord+1}')
                                
                               
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break
                        
                       
                       
                    #down
                    xform, yform = 0,0
                    while yform+rownum > 0:
                        #xform -= 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False:
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} Rook'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}R{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        else:
                            break 
                        
                        
                        
                        
                if item.endswith('King'):
                    
                    #left
                    xform, yform = 0,0
                    while xform+colnum > 0:
                        xform -= 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                            
                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                                
                        
                        break
                    
                    #right
                    xform, yform = 0,0
                    while xform+colnum < 6:
                        xform += 1
                        #yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        
                        break
                        
                    
                    
                    #up
                    xform, yform = 0,0
                    while yform+rownum < 6:
                        #xform -= 1
                        yform += 1
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        
                        break
                       
                       
                    #down
                    xform, yform = 0,0
                    while yform+rownum > 0:
                        #xform -= 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        break
                    
                    #up left
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum > 0:
                        xform -= 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        break
                        
                    #up right
                    xform, yform = 0,0
                    while yform+rownum < 6 and xform+colnum < 6:
                        xform += 1
                        yform += 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King' 
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        break
                    
                    #down left
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum > 0:
                        xform -= 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        break
                    
                    #down right
                    xform, yform = 0,0
                    while yform+rownum > 0 and xform+colnum < 6:
                        xform += 1
                        yform -= 1
                        
                        ycoord = yform+rownum
                        xcoord = xform+colnum

                        if board[ycoord][xcoord].startswith(color_turn) == False: 
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[ycoord][xcoord] = f'{color_turn} King'
                            if is_check(newboard, color_turn) == None:  
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}K{colum_letters[xcoord]}{ycoord+1}')
                                
                                
                                
                                boards.append(newboard)
                                
                                if board[ycoord][xcoord] != '_':
                                    break
                            
                        break
                
                if item.endswith('Knight'):
                    
                    for test in [[2,1],[-2,1],[2,-1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]:
                        
                        if rownum+test[0] not in range(0,8) or colnum+test[1] not in range(0,8): 
                            continue
                        
                        
                        
                        if board[rownum+test[0]][colnum+test[1]].startswith(color_turn) == False:
                            
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[rownum+test[0]][colnum+test[1]] = f'{color_turn} Knight'
                        
                        
                            if is_check(newboard, color_turn) == None:  
                                
                                
                                moves.append(f'{colum_letters[colnum]}{rownum+1}N{colum_letters[colnum+test[1]]}{rownum+test[0]+1}')
                                
                                boards.append(newboard)
                 
                 
                            
                if item.endswith('Pawn'):
                    
                    if color_turn == 'white':
                        if rownum+1 in range(0,8) and colnum+1 in range(0,8):
                     
                        
                            if board[rownum+1][colnum+1] != '_' and board[rownum+1][colnum+1].startswith('black'):
                                
                                newboard = copy.deepcopy(board)
                                newboard[rownum][colnum] = '_'
                                newboard[rownum+1][colnum+1] = f'{color_turn} Pawn'
                                if is_check(newboard, color_turn) == None:
                                    
                                    moves.append(f'{colum_letters[colnum+1]}{rownum+1+1}')
                                    boards.append(newboard)
                        
                        if rownum+1 in range(0,8) or colnum-1 in range(0,8):
                            
                           
                        
                            if board[rownum+1][colnum-1] != '_' and board[rownum+1][colnum-1].startswith('black'):
                                newboard = copy.deepcopy(board)
                                newboard[rownum][colnum] = '_'
                                newboard[rownum+1][colnum-1] = f'{color_turn} Pawn'
                                
                                if is_check(newboard, color_turn) == None:
                                    
                                    moves.append(f'{colum_letters[colnum-1]}{rownum+1+1}')
                                    boards.append(newboard)
                        
                        
                        if rownum+1 < 8 and board[rownum+1][colnum] == '_':
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[rownum+1][colnum] = f'{color_turn} Pawn'
                            
                            if is_check(newboard, color_turn) == None:    
                                moves.append(f'{colum_letters[colnum]}{rownum+1+1}')
                                boards.append(newboard)
                        
                        if rownum+2 < 8 and board[rownum+2][colnum] == '_':
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[rownum+2][colnum] = f'{color_turn} Pawn'
                            
                            if is_check(newboard, color_turn) == None:    
                                moves.append(f'{colum_letters[colnum]}{rownum+2+1}')
                                boards.append(newboard)
                            
                    if color_turn == 'black':
                        
                        if rownum-1 in range(0,8) and colnum+1 in range(0,8):
                     
                            
                        
                            if board[rownum-1][colnum+1] != '_' and board[rownum-1][colnum+1].startswith('white'):
                                newboard = copy.deepcopy(board)
                                newboard[rownum][colnum] = '_'
                                newboard[rownum-1][colnum+1] = f'{color_turn} Pawn'
                            
                                if is_check(newboard, color_turn) == None:
                                    
                                    moves.append(f'{colum_letters[colnum+1]}{rownum-1+1}')
                                    boards.append(newboard)
                        
                        if rownum-1 in range(0,8) or colnum-1 in range(0,8):
                            
                            
                        
                            if board[rownum-1][colnum-1] != '_' and board[rownum-1][colnum-1].startswith('white'):
                                newboard = copy.deepcopy(board)
                                newboard[rownum][colnum] = '_'
                                newboard[rownum-1][colnum-1] = f'{color_turn} Pawn'
                                if is_check(newboard, color_turn) == None:
                                    
                                    moves.append(f'{colum_letters[colnum-1]}{rownum-1+1}')
                                    boards.append(newboard)
                        
                        
                        if rownum-1 < 8 and board[rownum-1][colnum] == '_':
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[rownum-1][colnum] = f'{color_turn} Pawn'
                            
                            if is_check(newboard, color_turn) == None:    
                                moves.append(f'{colum_letters[colnum]}{rownum-1+1}')
                                boards.append(newboard)
                                
                        if rownum-2 < 8 and board[rownum-2][colnum] == '_':
                            newboard = copy.deepcopy(board)
                            newboard[rownum][colnum] = '_'
                            newboard[rownum-2][colnum] = f'{color_turn} Pawn'
                            
                            if is_check(newboard, color_turn) == None:    
                                moves.append(f'{colum_letters[colnum]}{rownum-2+1}')
                                boards.append(newboard)
                colnum+=1
    
    return moves
                
def is_checkmate(board, color_turn):
    

    if is_check(board, color_turn) == True:
        moves = get_legal_moves(board, color_turn)
        if len(moves) == 0:
            return True
        else:
            return False
    else:
        return False
        
def gameover(result, winner):
    print(result+'\n')
    print(f'Winner: {winner}')
    
def human_turn(human_color):
    global board
    global boards
    global color_turn

    for i in board:
        print(i)
    color_turn = human_color

    moves = get_legal_moves(board, human_color)
    if len(moves) == 0:
        if is_checkmate(board, human_color) == True:
            gameover(result = 'checkmate', winner = 'Computer')
            
        else:
            gameover(result = 'draw', winner = None)
            
        return 'stop'
        
    print('Your turn')
    move = ''
    while move not in moves:
        move = input(f'Legal Moves: {", ".join(moves)} \n')
        
    board = boards[moves.index(move)]
    
    for i in board:
        print(i)
    
    
def computer_turn(computer_color):
    global board
    global boards
    global computer_level
    global human_color
    global color_turn
    global check_tested
    global legal_move_tested
    
    color_turn = computer_color
    moves = get_legal_moves(board, computer_color)
    
    if len(moves) == 0:
        if is_check(board, computer_color) == True:
            gameover(result = 'checkmate', winner = 'Human')
            
        else:
            gameover(result = 'draw', winner = None)
            
        return 'stop'
    
    
    
    
    #save the board states corrisponding to the current moves, because "boards" is disposable and will be rewritten over many times before a move is chosen
    og_boards = copy.deepcopy(boards)
    
    #create an array to store the "value" for each legal move
    values = [0]*len(moves)
    
    #look "computer_level" moves into the future for each of the legal moves
    for index in range(len(og_boards)):
        print('index: '+str(index))
        timer = time.perf_counter()
        layer = []
        
        #one of the potential game states after computer's turn
        newboard = copy.deepcopy(og_boards[index])
        if is_checkmate(board, human_color) == True:
            values[index] += 100*computer_level
        
        # "human_options" is a garbage variable
        human_options = get_legal_moves(newboard, human_color)
        
        # "boards" now contains board states after human's turn
        
        #do a pair of turns for one less than "computer_level" iterations, store each set of board states inside of a "layer"

        layer = copy.deepcopy(boards)
        for i in range(1,computer_level+1):
            print('turns calculated: ' + str(i) + ' in ' + str(time.perf_counter()-timer) + ' seconds ')
            timer = time.perf_counter()
            print(len(layer))
            #current states in the layer
            
            
            states = copy.deepcopy(layer)
            
            
            layer = []
            watch = time.perf_counter()
            count = 0
            for state in states:
                #total = time.perf_counter()
                
                
                #penalize for checkmate states, 100 for each turn checkmated
                
                if is_checkmate(state, computer_color) == True:
                    values[index] -= 100*(computer_level-i)
                    continue
                
                computer_options = get_legal_moves(state, computer_color)
                

                assess = True
                for option in boards:
                    if is_checkmate(option, human_color) == True:
                        values[index] += 100*(computer_level-i)
                        continue
                    
                    else:
                
                        
                        
                        #watch = time.perf_counter()
                        
                        #minmax the boards that are most important
                        human_options = get_legal_moves(option, human_color)
                        if i < computer_level:
                            
                            top = []
                            scores = [10000]
                            for test in boards:
                                if count%200 == 0 and test== boards[-1]:
                                    looptime = time.perf_counter()
                                score = 0
                                #tick = time.perf_counter()
                                if is_checkmate(test, computer_color) == True:
                                    top.insert(0,test)
                                    scores.insert(0,-100)
                                    
                                #print(f'ischekmatestep: {time.perf_counter()-tick}')
                                #tick = time.perf_counter()
                                
                                if is_check(test, computer_color) == True:
                                    score = -2
                                    
                                #print(f'ischeckstep: {time.perf_counter()-tick}')
                                #tick = time.perf_counter()
                                
                                for row in test:
                                    for item in row:
                                        if item == '_' or item.endswith('King'):
                                            continue
                                        
                                        if item.endswith('Bishop') or item.endswith('Knight'):
                                            points = 3
                                        elif item.endswith('Rook'):
                                            points = 5
                                        elif item.endswith('Queen'):
                                            points = 9
                                        elif item.endswith('Pawn'):
                                            points = 1
                                        
                                        if item.startswith(computer_color):
                                            score += points
                                        else:
                                            score -= points
                                
                                #print(f'readboardstep: {time.perf_counter()-tick}')
                                #tick = time.perf_counter()
                                
                                comp_pos = 0
                                while score > scores[comp_pos] and comp_pos <= len(scores)-1:
                                    comp_pos+=1
                                scores.insert(comp_pos, score)
                                top.insert(comp_pos, test)    
                            
                                #print(f'insertassess: {time.perf_counter()-tick}')
                                if count%200 == 0 and test== boards[-1]:
                                    print(f'loop: {time.perf_counter()-looptime}')
                            #print(scores[:11])
                            boards = top[:5]
                            
                        
                        
                        if count%200 == 0 and assess == True:
                            
                            print((time.perf_counter()-watch)/200, time.perf_counter()-watch)
                            watch= time.perf_counter()
                            """
                            print('get_legal_moves in '+str(time.perf_counter()-watch))
                            watch = time.perf_counter()
                            is_check(boards[0], computer_color)
                            print('is_check in '+str(time.perf_counter()-watch))
                            print('check checked '+str(check_tested)+' times')
                            print('moves found '+str(legal_move_tested)+' times')
                            """
                            print(f'{count}/{len(states)}')

                            assess = False
                        
                        layer += boards
                        
                        
                count+=1
                #print(time.perf_counter()-total)
                
                
                
    #add up peices to tally the value of the board state.
    for state in layer:
        for row in state:
            for item in row:
                if item == '_' or item.endswith('King'):
                    continue
                
                
                if item.endswith('Bishop') or item.endswith('Knight'):
                    points = 3
                elif item.endswith('Rook'):
                    points = 5
                elif item.endswith('Queen'):
                    points = 9
                elif item.endswith('Pawn'):
                    points = 1
                
                if item.startswith(computer_color):
                    values[index] += points
                else:
                    values[index] -= points
        
    best = values[0]
    index = 0
    for i in range(1,len(values)):
        if values[i] > best:
            best = values[i]
            index = i
    
    
    board = og_boards[index]
    print(f'The computer played {moves[index]}.')
                
    

def game(human_color, computer_color, computer_level):
    
	#state = computer_turn(computer_color)
	if human_color == 'white':
		while True:
			state = human_turn(human_color)
			
			if state == 'stop':
				break
			
			state = computer_turn(computer_color)
			
			if state == 'stop':
				break
        
	else:
		while True:
			state = computer_turn(computer_color)
			
			if state == 'stop':
				break
			
			state = human_turn(human_color)
			
			if state == 'stop':
				break
		
        
def setup():
    global computer_level
    human_color = ''
    while human_color not in ['white','black']:
        human_color = input('Play as white or black?\n>  ')
        
    computer_color = ['white','black']
    computer_color.remove(human_color)
    
    computer_color = ''.join(computer_color)
    
    computer_level = -1
    while computer_level not in range(1,11):
        computer_level = int(input('Computer level (1-10):\n>  '))
        
    game(human_color, computer_color, computer_level)
        

setup()