#!/usr/bin/env python
# coding: utf-8

# In[16]:

import numpy as np
import random
import math

nrows = 6
ncols = 7

player = 0
AI = 1

empty = 0
player_coin = 1
AI_coin = 2

game_length = 4


def create_board():
    board = np.zeros((nrows, ncols))
    return board

def move(board, row, col, coin):
    board[row][col] = coin

def valid_move(board, col):
    return board[nrows - 1][col] == 0

def next_empty_row(board, col):
    for row in range(nrows):
        if board[row][col] == 0:
            return row

# won't work without argument 
def flip_board(board): 
    print(np.flip(board, 0))

def winning_move(board, coin):
    #check horizontally
    for c in range(ncols - 3):
        for r in range(nrows):
            if board[r][c] == coin and board[r][c + 1] == coin and board[r][c + 2] == coin and board[r][c + 3] == coin:
                return True

    #check vertically
    for c in range(ncols):
        for r in range(nrows - 3):
            if board[r][c] == coin and board[r + 1][c] == coin and board[r + 2][c] == coin and board[r + 3][c] == coin:
                return True

    #check positive slope:
    for c in range(ncols - 3):
        for r in range(nrows - 3):
            if board[r][c] == coin and board[r + 1][c + 1] == coin and board[r + 2][c + 2] == coin and board[r + 3][c + 3] == coin:
                return True
    
    #check negative slope:
    for c in range(ncols - 3):
        for r in range(3, nrows):
            if board[r][c] == coin and board[r - 1][c + 1] == coin and board[r - 2][c + 2] == coin and board[r - 3][c + 3] == coin:
                return True

def eval_game(game, coin):
    score = 0
    opp_coin = player_coin
    if coin == player_coin:
        opp_coin = AI_coin
    
    if game.count(coin) == 4:
        score += 100
    elif game.count(coin) == 3 and game.count(empty) == 1:
        score += 5
    elif game.count(coin) == 2 and game.count(empty) == 2:
        score += 2
    
    if game.count(opp_coin) == 3 and game.count(empty) == 1:
        score -= 4
    return score

def score_position(board, coin):
    score = 0

    #check center column
    center_arr = [(int) for i in list(board[:, ncols // 2])]
    center_count = center_arr.count(coin);
    score += center_count * 3

    #check horizontal
    for r in range(nrows):
        row_arr = [(int) for i in list(board[r, :])]
        for c in range(ncols - 3):
            game = row_arr[c : c + game_length]
            score += eval_game(game, coin)

    #check vertical
    for c in range(ncols):
        col_arr = [(int) for i in list(board[:, c])]
        for r in range(nrows - 3):
            game = col_arr[r : r + game_length]
            score += eval_game(game, coin)

    #check positive slope
    for r in range(nrows - 3):
        for c in range(ncols - 3):
            game = [board[r + i][c + i] for i in range(game_length)]
            score += eval_game(game, coin)

    #check negative slope
    for r in range(nrows - 3):
        for c in range(ncols - 3):
            game = [board[r + 3 - i][c + i] for i in range(game_length)]
            score += eval_game(game, coin)
    
    return score

def terminal_node(board):
    return winning_move(board, player_coin) or winning_move(board, AI_coin) or len(get_valid_locations(board)) == 0

def minimax(board, alpha, beta, depth, maximising_player):
    valid_locations = get_valid_locations(board)
    is_terminal = terminal_node(board)
    if is_terminal or depth == 0:
        if is_terminal:
            if winning_move(board, AI_coin):
                return (None, 100000000000)
            elif winning_move(board, player_coin):
                return (None, -100000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_coin))
    if maximising_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_empty_row(board, col)
            b_temp = board.copy()
            move(b_temp, row, col, AI_coin)
            score = minimax(b_temp, alpha, beta, depth - 1, False)[1]
            if score > value:
                value = score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = next_empty_row(board, col)
            b_temp = board.copy()
            move(board, row, col, player_coin)
            score = minimax(b_temp, alpha, beta, depth - 1, True)[1]
            if score < value:
                value = score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(ncols):
        if valid_move(board, col):
            valid_locations.append(col);
    return valid_locations

def pick_best_move(board, coin):
    valid_locations = get_valid_locations(board) 
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = next_empty_row(board, col)
        b_temp = board.copy()
        move(temp_board, row, col, coin)
        score = score_position(b_temp, coin);
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

board = create_board()
flip_board(board)

game_over = False;

turn = random.randint(player, AI)

while not game_over:
    if turn == player:
        col = int(input('Your turn. Please enter a column number between 0 and 6 inclusive: '))
        if valid_move(board, col):
            row = next_empty_row(board, col)
            move(board, row, col, player_coin)

            flip_board(board)

            if winning_move(board, player_coin):
                print('Player 1 wins!!')
                game_over = True
            
            turn += 1
            turn = turn % 2
    
    if turn == AI and not game_over:
        print('Thinking.....')
        col, minimax_score = minimax(board, -math.inf, math.inf, 5, True)
        if valid_move(board, col):
            row = next_empty_row(board, col)
            move(board, row, col, AI_coin)

            flip_board(board)

            if winning_move(board, AI_coin):
                print('AI wins!!')
                game_over = True

            turn += 1
            turn = turn % 2
