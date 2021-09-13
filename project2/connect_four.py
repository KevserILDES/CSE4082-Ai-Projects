import random

##################################################################

row_num = 6
column_num = 7

##################################################################

#Connect4 play game class
class Connect4(object):
    def __init__(self,players,turn):
        #initialize values and game board
        self.board=[[' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' ']]
        self.is_game_over = False
        self.winner = None
        self.turn = turn
        self.round = 1
        self.players = players

    #method to switch turn and increment round in each run
    def switch_players_turn_and_inc_round(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        self.round += 1

    #method to place each piece on board
    def nextMove(self):
        #define player to make a move
        current_player = self.turn

        if self.round > column_num * row_num:
            self.is_game_over = True
            return
        
        #take action of according player
        move = current_player.move(self.board)
        
        #make move if valid, check winning condition and switch turn to other player
        for i in range(row_num):
            #if there is empty place put according sign
            if self.board[i][move] == ' ':
                self.board[i][move] = current_player.sign
                self.switch_players_turn_and_inc_round() #increment round and pass to other player
                self.check_fours(i,move) #check if it is a winning move

                if self.round > column_num * row_num: #if all possible actions end and no place in board end game
                    self.is_game_over = True
            
                #print state of the board accordingly
                if not self.is_game_over:
                    self.printState()
                else:
                    self.printFinishState()

                return

        print("That column is full. Please try another one!")
        return
    
    #check fours in all directions and end game if any
    def check_fours(self,row,col):
        if self.horizontal_check(row,col) or self.vertical_check(row,col) or self.diagonal_check(row,col):
            self.is_game_over=True
            return

    #method to assign winner if game is over
    def check_winner(self, curr_row, curr_column):
        if self.players[0].sign == self.board[curr_row][curr_column]:
            self.winner = self.players[0]
        else:
            self.winner = self.players[1]
        
    #check if there is 4 in vertical direction according to piece location entered
    def vertical_check(self, curr_row, curr_column):
        count = 0
        max_count = 0
        sign = self.board[curr_row][curr_column]
        check_4 = False
        
        #check if there is 4 equal sign on that column
        for i in range(row_num):
            if self.board[i][curr_column] == sign:
                count += 1 
            else:
                if count > max_count:
                    max_count = count
                count = 0
        if max_count >= 4 or count >= 4:
            check_4 = True
            self.check_winner(curr_row, curr_column)
        return check_4
    
    #check if there is 4 in horizontal direction according to piece location entered
    def horizontal_check(self, curr_row, curr_column):
        sign = self.board[curr_row][curr_column]
        check_4 = False
        count = 0
        max_count = 0
        #check if there is 4 equal sign on that row
        for i in range(column_num):
            if self.board[curr_row][i] == sign:
                count += 1 
            else:
                if max_count < count:
                    max_count = count
                count = 0
        if max_count >= 4 or count >= 4:
            check_4 = True
            self.check_winner(curr_row, curr_column)
        return check_4
    
    #check if there is 4 in diagonal direction according to piece location entered
    def diagonal_check(self, curr_row, curr_column):
        sign = self.board[curr_row][curr_column]
        check_4 = False
        count1 = 1
        col = curr_column
        rw = curr_row
        j = 1
        br_1 = 1
        br_2 = 1
        # to check diagonal move in '/' direction
        #if there is total 3 equal sign together in next to current put one        
        for i in range(1, row_num):
            #for move placed in board as row and col, search for (row+1, col+1)s -through upper diagonal
            if (rw+i <= 5) and (col+j <= 6) and (self.board[rw+i][col+j] == sign) and br_1 == 1:
                count1 += 1
            else: #if there is no more equal sign stop counting for that part
                br_1 = 0
            #and search for (row-1,col-1)s -through down diagonal -
            if (rw-i >= 0) and(col-j >= 0) and self.board[rw-i][col-j] == sign and br_2 == 1:
                count1 += 1
            else: #if there is no more equal sign stop counting for that part
                br_2 = 0
            if br_1 == 0 and br_2 == 0:
                break
            j += 1
           
        #if there are 4 of that sign assign winner
        if count1 >= 4:
            check_4 = True
            self.check_winner(curr_row, curr_column)
            return check_4
            
        count2 = 1
        col = curr_column
        rw = curr_row
        j=1
        br_1=1
        br_2=1
        # to check diagonal move in '\' direction
        #if there is total 3 equal sign together in next to current put one
        for i in range(1,row_num):
            #for move placed in board as row and col, search for (row-1, col+1)s -through down diagonal
            if (rw-i >= 0) and (col+j <= 6) and (self.board[rw-i][col+j] == sign) and br_1 == 1:
                count2 += 1
            else: #if there is no more equal sign stop counting for that part
                br_1 =0  
            #and search for (row+1,col-1)s -through upper diagonal -
            if (rw+i <= 5) and(col-j >= 0) and self.board[rw+i][col-j] == sign and br_2 == 1:
                count2 += 1
            else: #if there is no more equal sign stop counting for that part
                br_2 = 0
            if br_1 == 0 and br_2 == 0:
                break
            j += 1
        
        #if there are 4 of that sign assign winner
        if count2 >= 4:
            check_4 = True
            self.check_winner(curr_row, curr_column)
        return check_4
    
    #method to print board on console
    def printState(self):
        if not self.is_game_over:
            print("\nRound: " + str(self.round))
    
            if self.turn == self.players[0]:
                turn_of_the_player = 1
            else:
                turn_of_the_player = 2
            print("It's player " + str(turn_of_the_player) + "'s turn:")

        for i in range(5, -1, -1):
            for j in range(column_num):
                print("| " + str(self.board[i][j]), end = " ")
            print("|")
        print("  1   2   3   4   5   6   7 ")

    #method to print final info after game over
    def printFinishState(self):
        print("\nGame over!")
        if self.winner != None:
            if self.turn == self.players[0]:
                winner = 2
            else:
                winner = 1
            print("Player",  str(winner), "is the winner!")
        else:
            print("Nobody wins! It is a draw!")
        
        self.printState()

##################################################################
#class for human player of the game
class HumanPlayer(object):

    def __init__(self, sign):
        self.type = "Human"
        self.sign = sign
    
    #method for action of human player, it simply asks player for column number 
    def move(self, state):
        column = 0
        while True:
            column_choice = int(input("Enter a column number you want to put your sign: ")) - 1
            if 0 <= column_choice <= row_num:
                column = column_choice
                break
            else:
                print("Invalid! Please try again!")
        return column

##################################################################
#class for ai player of the game
class AIPlayer(HumanPlayer):
    def __init__(self, sign, depth, heuristic, minimax_option):
        self.type = "AI"
        self.sign = sign
        self.depth=depth
        self.heuristic = heuristic
        self.minimax_option = minimax_option
        
    #method for action of ai player, it decides action according to minimax algorithm
    def move(self, state):
        if self.minimax_option == 1:
            m = Minimax_1(state, self.sign,self.heuristic)
            best_move, value = m.bestMove(state,self.depth + 1, self.sign)
            return best_move
        else:
            m = Minimax_2(state,self.sign,self.heuristic)
            best_move, value = m.bestMove(state,self.depth + 1, self.sign)
            return best_move
##################################################################
import math
import copy

#class for classic minimax
class Minimax_1:    
    def __init__(self, board, sign, heuristic):
        self.game_board = copy.deepcopy(board)
        self.sign = sign
        self.heuristic = heuristic
          
    #method to find all columns available 
    def valid_moves(self, board):
        actions = []
        for i in range(column_num):
            if board[row_num-1][i] == ' ':
                actions.append(i)
        return actions
    
    #method to find best move
    def bestMove(self, board, depth, curr_sign):
        # determine opponent's sign
        if curr_sign == 'X': opp_sign = 'O' #assign players for min max
        else: opp_sign = 'X'
        
        #take empty columns
        validMoves = self.valid_moves(board)
        
        #find possible moves and corresponding scores and according boards
        moves = {}
        for i in validMoves:
            temp = self.makeMove(board,i,curr_sign)
            moves[i] = -self.search(temp,depth-1,opp_sign)
        
        #find best-value-move in all moves
        best_alpha = -math.inf
        best_move = None
        moves = moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha
        
    #to determine score
    def search(self, board, depth, curr_sign):

        validMoves = self.valid_moves(board)
        moves = []
        for i in validMoves:
            temp = self.makeMove(board, i, curr_sign)
            moves.append(temp)
                
        # if game is over or depth == 0
        if depth == 0 or len(moves) == 0 or self.gameOver(board):
            # return the heuristic value of node
            return self.evaluate(board, curr_sign)
        
        # determine opponent's sign
        if curr_sign == 'X': opp_sign = 'O' #assign players
        else: opp_sign = 'X'

        #recursive call to find best score
        alpha = -math.inf
        for i in moves:
            if i == None:
                print("move == None (search)")
            alpha = max(alpha, - self.search(i, depth - 1, opp_sign))
        return alpha

    #check if there is 4 of same sign and end game if any
    def gameOver(self,board):
        if self.countSigns(board, 'X', 4) >= 1 or self.countSigns(board,'O',4) >= 1:
            return True
        return False
        
    #create according board making given move
    def makeMove(self, state, column, sign):
        temp =  copy.deepcopy(state)
        for i in range(row_num):
            if temp[i][column] == ' ':
                temp[i][column] = sign
                return temp

    #evaluation method for minimax, returns score according to given heuristic
    def evaluate(self,board,sign):
        if self.heuristic == 0:
            return self.heuristic1(board,sign)
        elif self.heuristic == 1:
            return self.heuristic2(board,sign)
        else:
            return self.heuristic3(board,sign)
        
    #first heuristic method
    def heuristic1(self, state, sign):
        if sign == 'X': opp_sign = 'O' 
        else: opp_sign = 'X'
        
        curr_fours = self.countSigns(state, sign, 4)
        curr_threes = self.countSigns(state, sign, 3)
        curr_twos = self.countSigns(state, sign, 2)
        opp_fours = self.countSigns(state, opp_sign, 4)

        if opp_fours > 0:
            return -math.inf
        else:
            return curr_fours * 100000 + curr_threes * 100 + curr_twos

    #second heuristic method  
    def heuristic2(self,board,sign):
        if sign == 'X': opp_sign = 'O' 
        else: opp_sign = 'X'
        
        curr_fours = self.countSigns(board, sign, 4)
        curr_threes = self.countSigns(board, sign, 3)
        curr_twos = self.countSigns(board, sign, 2)
        opp_fours = self.countSigns(board, opp_sign, 4)
        opp_threes = self.countSigns(board, opp_sign, 3)
        opp_twos = self.countSigns(board, opp_sign, 2)
        
        opp_score = (opp_fours*100000 + opp_threes*1000 + opp_twos)
        curr_score = (curr_fours*100000 + curr_threes*1000 + curr_twos)

        if opp_score > curr_score:
            return -opp_score
        else:
            return curr_score 
        
    #third heuristic method
    def heuristic3(self,board,sign):
        if sign == 'X': opp_sign = 'O' 
        else: opp_sign = 'X'
        
        curr_fours = self.countSigns(board, sign, 4)
        curr_threes = self.countSigns(board, sign, 3)
        curr_twos = self.countSigns(board, sign, 2)
        opp_fours = self.countSigns(board, opp_sign, 4)
        opp_threes = self.countSigns(board, opp_sign, 3)
        opp_twos = self.countSigns(board, opp_sign, 2)
        
        opp_score = (opp_fours*100000 + opp_threes*1000 + opp_twos)
        curr_score = (curr_fours*100000 + curr_threes*1000 + curr_twos)

        if opp_fours > 0:
            return -math.inf
        elif opp_score>curr_score:
            return -opp_score
        else:
            return curr_score-opp_score
        
    #sum all counts of given number of equal sign in each direction 
    def countSigns(self, board, sign, count):
        counter = 0
        for i in range(row_num):
            for j in range(column_num):
                if board[i][j] == sign:
                    counter += self.vertical_check(i, j, board, count)
                    counter += self.horizontal_check(i, j, board, count)
                    counter += self.diagonal_check(i, j, board, count)
        # return the sum of streaks of size count
        return counter
          
    #check all consecutive equal sign in vertical direction and return 1 if there is at least given number of equals 
    def vertical_check(self, curr_row, curr_column, board, count):
        consecutiveCount = 0
        for i in range(curr_row, row_num):
            if board[i][curr_column] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= count:
            return 1
        else:
            return 0
    
    #check all consecutive equal sign in horizontal direction and return 1 if there is at least given number of equals 
    def horizontal_check(self, curr_row, curr_column, board, count):
        consecutiveCount = 0
        for j in range(curr_column, column_num):
            if board[curr_row][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= count:
            return 1
        else:
            return 0
    
    #check all consecutive equal sign in diagonal direction and return 1 if there is at least given number of equals 
    def diagonal_check(self, curr_row, curr_column, board, count):
        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = curr_column
        for i in range(curr_row, row_num):
            if j > row_num:
                break
            elif board[i][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
            j += 1
            
        if consecutiveCount >= count:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = curr_column
        for i in range(curr_row, -1, -1):
            if j > row_num:
                break
            elif board[i][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
            j += 1

        if consecutiveCount >= count:
            total += 1

        return total
    
#minimax class with alpha beta pruning
class Minimax_2:
    def __init__(self, board, sign, heuristic):
        self.signs = ["X", "O"]
        self.game_board = copy.deepcopy(board)
        self.sign = sign
        self.heuristic = heuristic

    #method to find all columns available 
    def valid_moves(self, board):
        actions = []
        for i in range(column_num):
            if board[row_num-1][i]==' ':
                actions.append(i)
        return actions
    
    #first heuristic method
    def heuristic1(self,board,sign):
        if sign=='X': opp_sign='O' 
        else: opp_sign='X'
        
        curr_fours = self.countSigns(board, sign, 4)
        curr_threes = self.countSigns(board, sign, 3)
        curr_twos = self.countSigns(board, sign, 2)
        opp_fours = self.countSigns(board, opp_sign, 4)

        if opp_fours > 0:
            return -100000
        else:
            score=curr_fours * 100000 + curr_threes * 100 + curr_twos
            """if score==0:
                return random.randint(1,10)
            """
            return score

    #second heuristic method  
    def heuristic2(self,board,sign):
        if sign == 'X': opp_sign = 'O' 
        else: opp_sign = 'X'
        
        curr_fours = self.countSigns(board, sign, 4)
        curr_threes = self.countSigns(board, sign, 3)
        curr_twos = self.countSigns(board, sign, 2)
        opp_fours = self.countSigns(board, opp_sign, 4)
        opp_threes = self.countSigns(board, opp_sign, 3)
        opp_twos = self.countSigns(board, opp_sign, 2)
        
        if opp_fours > 0:
            return -math.inf
        else:
            score=((curr_fours*100000 + curr_threes*1000 + curr_twos*100) - 
                    (opp_fours*100000 + opp_threes*1000 + opp_twos*100))
            if score==0:
                return  random.randint(1,10)
            
            return score 
        
    #third heuristic method
    def heuristic3(self,board,sign):
        if sign=='X': opp_sign='O' 
        else: opp_sign='X'
        
        curr_fours = self.countSigns(board, sign, 4)
        curr_threes = self.countSigns(board, sign, 3)
        curr_twos = self.countSigns(board, sign, 2)
        opp_fours = self.countSigns(board, opp_sign, 4)
        opp_threes = self.countSigns(board, opp_sign, 3)
        opp_twos = self.countSigns(board, opp_sign, 2)
        
        opp_score=(opp_fours*100000 + opp_threes*1000 + opp_twos)
        curr_score=(curr_fours*100000 + curr_threes*1000 + curr_twos)
        if opp_fours > 0:
            return -math.inf
        elif opp_score>curr_score:
            return -opp_score
        else:
            return curr_score-opp_score

    #evaluation method for minimax, returns score according to given heuristic
    def evaluate(self,board,sign):
        if self.heuristic==0:
            return self.heuristic1(board,sign)
        elif self.heuristic==1:
            return self.heuristic2(board,sign)
        else:
            return self.heuristic3(board,sign)
        
    #sum all counts of given number of equal sign in each direction 
    def countSigns(self, board, sign, count):
        counter = 0
        for i in range(row_num):
            for j in range(column_num):
                if board[i][j] == sign:
                    counter += self.vertical_check(i, j, board, count)
                    counter += self.horizontal_check(i, j, board, count)
                    counter += self.diagonal_check(i, j, board, count)
        # return the sum of streaks of size count
        return counter
            
    #check all consecutive equal sign in vertical direction and return 1 if there is at least given number of equals 
    def vertical_check(self, curr_row, curr_column, board, count):
        consecutiveCount = 0
        for i in range(curr_row, row_num):
            if board[i][curr_column] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= count:
            return 1
        else:
            return 0
    
    #check all consecutive equal sign in horizontal direction and return 1 if there is at least given number of equals 
    def horizontal_check(self, curr_row, curr_column, board, count):
        consecutiveCount = 0
        for j in range(curr_column, column_num):
            if board[curr_row][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= count:
            return 1
        else:
            return 0

    #check all consecutive equal sign in diagonal direction and return 1 if there is at least given number of equals 
    def diagonal_check(self, curr_row, curr_column, board, count):
        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = curr_column
        for i in range(curr_row, row_num):
            if j > row_num:
                break
            elif board[i][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
            j += 1
            
        if consecutiveCount >= count:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = curr_column
        for i in range(curr_row, -1, -1):
            if j > row_num:
                break
            elif board[i][j] == board[curr_row][curr_column]:
                consecutiveCount += 1
            else:
                break
            j += 1

        if consecutiveCount >= count:
            total += 1

        return total
       
    #check if there is 4 of same sign and end game if any
    def gameOver(self,board):
        if self.countSigns(board, 'X', 4) >= 1 or self.countSigns(board,'O',4)>=1:
            return True
        return False
        
    #create according board making given move
    def makeMove(self, state, column, sign):
        temp = copy.deepcopy(state)
        for i in range(row_num):
            if temp[i][column] == ' ':
                temp[i][column] = sign
                return temp,i,column

    #method to find all columns available 
    def bestMove(self,board, depth, sign):
        # get all valid moves and shuffle randomly 
        validMoves = self.valid_moves(board)
        random.shuffle(validMoves)
        bestMove  = validMoves[0]
        bestScore = float("-inf")
    
        # initialize values for alpha-beta pruning
        alpha = float("-inf")
        beta = float("inf")
    
        #define opponent's sign
        if sign == 'X': opponent = 'O'
        else: opponent = 'X'
      
        # create board for all possible moves and calculate scores
        for move in validMoves:
            tempBoard = self.makeMove(board, move, sign)[0]
            # take score from min function
            boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, beta, sign, opponent)
            if boardScore > bestScore:
                bestScore = boardScore
                bestMove = move
        return bestMove,bestScore
    
    #minimize function
    def minimizeBeta(self, board, depth, a, b, sign, opponent):
        
        validMoves = self.valid_moves(board)
        # if game is over or depth == 0
        if depth == 0 or len(validMoves) == 0 or self.gameOver(board):
            return self.evaluate(board, sign)
        
        validMoves = self.valid_moves(board) 
        beta = b
        
        #go through all as long as condition met
        for move in validMoves:
            boardScore = float("inf")
            if a < beta:
                tempBoard = self.makeMove(board, move, opponent)[0]
                boardScore = self.maximizeAlpha(tempBoard, depth - 1, a, beta, sign, opponent)
    
            if boardScore < beta:
                beta = boardScore
        return beta
    
    #maximize function
    def maximizeAlpha(self, board, depth, a, b, sign, opponent):
        validMoves=self.valid_moves(board)
        # if game is over or depth == 0
        if depth == 0 or len(validMoves) == 0 or self.gameOver(board):
            return self.evaluate(board, sign)
    
        alpha = a        

        #go through all as long as condition met
        for move in validMoves:
            boardScore = float("-inf")
            if alpha < b:
                tempBoard = self.makeMove(board, move, sign)[0]
                boardScore = self.minimizeBeta(tempBoard, depth - 1, alpha, b, sign, opponent)
    
            if boardScore > alpha:
                alpha = boardScore
        return alpha  

def minimax_options_AI ():
    # choose which minimax will be used by the AI
    choice = int(input("Enter minimax option for this AI (1 for normal - 2 for with alpha beta prunning): "))
    if choice == 1 or choice == 2:
        return choice
    else:
        print("Invalid! Default normal minimax will be used!")
        return 1
        
#method to take parameters of AI
def options_AI(sign):
    depth = int(input("Enter depth for this AI (1-4): "))
    if depth in [1,2,3,4,5,6,7,8,9,10]:
        heuristic= int(input("Enter heuristic option for this AI (1, 2, 3): "))-1
        if heuristic not in [0,1,2]:
            print("Invalid! Default 1 will be used")
            minimax_option = minimax_options_AI()
            return AIPlayer(sign, depth, 0, minimax_option)
        else:
            minimax_option = minimax_options_AI()
            return AIPlayer(sign, depth, heuristic, minimax_option)
    else:
        print("Invalid! Default 4 will be used!")
        heuristic= int(input("Enter heuristic option for this AI (1, 2, 3): "))-1
        if heuristic not in [0,1,2]:
            print("Invalid! Default 1 will be used")
            minimax_option = minimax_options_AI()
            return AIPlayer(sign, depth, 0, minimax_option)
        else:
            minimax_option = minimax_options_AI()
            return AIPlayer(sign, 4, heuristic, minimax_option)

def main():
    players=[None,None]
    #choose player1
    print("-> Choose player 1 - Human or AI")
    player_1 = int(input("Enter 1 for human, 2 for AI: "))
    if player_1 == 1:
        players[0] = HumanPlayer('X')
    elif player_1 == 2:
        sign='X'
        players[0]=options_AI(sign)            
    else:
        print("Invalid! Default Human will be used!")
        players[0] = HumanPlayer('X')
        
    #choose player2
    print("-> Choose player 2 - Human or AI")
    player_2 = int(input("Enter 1 for human, 2 for AI: "))
    if player_2 == 1:
        players[1] = HumanPlayer('O')
    elif player_2 == 2:
        sign='O'
        players[1]=options_AI(sign)
    else:
        print("Invalid! Default Human will be used!")
        players[1] = HumanPlayer('O')

    # choose the order of the players
    print("Who is going to start first?")
    choice = int(input("Enter 1 for player1 - 2 for player2: "))
    if choice == 1 or choice == 2:
        turn = players[choice - 1]
    else:
        print("Invalid! Default Player1 will be used!")
        turn = players[0]
    
    game = Connect4(players,turn)
    game.printState()
    
    while not game.is_game_over:
        game.nextMove()
        
if __name__ == "__main__":
    main()
    