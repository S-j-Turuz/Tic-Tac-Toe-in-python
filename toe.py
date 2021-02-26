from tkinter import *
#from tkinter import messagebox
import tkinter.messagebox
from tkinter import filedialog
import copy
from threading import Timer
import time 


root = Tk()
root.title("TIC TAC TOE")
#root.iconbitmap("/Users/anonymous/code/python/tic-tac-toe/tic.ico")
root.resizable(False, False)

# X starts -> x = True
X_player = True 
count = 0 #a winner can be established only after 4 moves. count to 4, then call check_winner every iteration.

#ai player
def O_player():
    global board, board_status, button_list
    available_buttons = [ ]#copies board_status as a single list to ls


#cheking who won
def check_winner(btn):
    global button_list, board_status, board
    game_over = False
    winner = False
    winner_name = None

    #checks for row win
    row_win_index = 0
    row_win_check = [ ]
    for row in board_status:#row is a--list of strings--nested inside  inside board_status
         #index of winning row
        if row[0] != '':#can't declare a row winner if the row isn't full
            if len(set(row)) == 1:# winning row all the same: cant have duplicates in a set
                winner = True
                winner_name = row[0]
                # if row == board[btn][0] board[btn][0] button_list[row is constant][col change].config(bg="green")
                for col_index in range(len(button_list)):# col_index: 0 -> 1 -> 2
                    button_list[row_win_index][col_index].config(highlightbackground="red")# coloring winning row in red
        row_win_index+=1
        

    #traversing rows and col
    col_as_row = [[board_status[col][row] for col in range(len(board_status))] for row in range(len(board_status)) ]

    #checks for column win
    col_win_index=0
    for col in col_as_row:#col is a nested list inside col_as_row.
        if col[0] != '':#can't declare a column winner if the column isn't full
            if len(set(col)) == 1:
                winner = True
                winner_name = col[0]
                #winning column col_index is constant, and row_index iterates from start to finish.
                for row_index in range(len(button_list)):# row_index: 0 -> 1 -> 2
                    button_list[row_index][col_win_index].config(highlightbackground="red")# coloring winning column in red
        col_win_index += 1
        


    #list with item position in left diagonal
    left_diagonal =[board_status[row][row] for row in range(len(board_status)) ]
    
    #list with item position in right diagonal
    right_diagonal =[board_status[row][len(board_status)-1 -row] for row in range(len(board_status))]
    
    #checks for diag win
    if '' not in left_diagonal:#checking left diagonal is all clicked
        if len(set(left_diagonal)) == 1:#sets don't allow duplicates so if all values are the same: length will be 1.
            winner = True
            winner_name = left_diagonal[0]
            #index behavior: [0][0] -> [1][1] -> [2][2] 
            for row_index in range(len(button_list)):# row_index: 0 -> 1 -> 2
                    button_list[row_index][row_index].config(highlightbackground="red")# coloring winning buttons in red

    if '' not in right_diagonal:#checking left diagonal is all clicked
        if len(set(right_diagonal)) == 1:#sets don't allow duplicates so if all values are the same: length will be 1.
            winner = True
            winner_name = right_diagonal[0]
            #index behavior: [0][2] -> [1][1] -> [2][0] 
            for row_index in range(len(button_list)):# row_index: 0 -> 1 -> 2
                    button_list[row_index][len(button_list) - 1 - row_index].config(highlightbackground="red")# coloring winning buttons in red
    
    if winner:# sending the name of the winner.
        st = f"Winner, winner, chicken dinner.\n{winner_name} won!!! wooooo"
        #call_end = Timer(0.01,end_game, st) #using timer so final board is rendered before message is shown
        #call_end.start()
        end_game(st) 
    else:
        ls = [item for elem in board_status for item in elem]#copies board_status as a single list to ls
        if len(set(ls)) ==3:
            game_over=False
        else:
            game_over=True
        if game_over:
            end_game("tie game")






# ROW WINNING POSSIBILITIES: ltr
# top row win:    [row=0 col=0, row=0 col=1, row=0 col=2] -> btn1, btn2, btn3 -> [0][0], [0][1], [0][2]
# mid row win:    [row=1 col=0, row=1 col=1, row=1 col=2] -> btn4, btn5, btn6 -> [1][0], [1][1], [1][2]
# bottom row win: [row=2 col=0, row=2 col=1, row=2 col=2] -> btn7, btn8, btn9 -> [2][0], [2][1], [2][2]

# COLUMN WINNING POSSIBILITIES: ltr
# left col win:  [row=0 col=0, row=1 col=0, row=2 col=0] -> btn1, btn4, btn7
# mid col win:   [row=0 col=1, row=1 col=1, row=2 col=1] -> btn2, btn5, btn8
# right col win: [row=0 col=2, row=1 col=2, row=2 col=2] -> btn3, btn6, btn9

# DIAGNAL WINNING POSSIBILITIES: ltr
# left diagnal win: [row=0 col=0, row=1 col=1, row=2 col=2] -> btn1, btn5, btn9
# right diagal win: [row=0 col=2, row=1 col=1, row=2 col=0] -> btn3, btn5, btn7
    
# the are 8 winning possibilities for 2 players: meaning 16 checks every iteration of the mainloop
#btn["text"] in row == same
#btn["text"] in col == same
#btn["text"] in diag == same


#disabling all the buttons
def disable_all_buttons():
    global button_list

    for btn_list in button_list:
        for btn in btn_list:
            btn.config(state="disabled")



#button clicked function
def b_click(b):
    global X_player, count, board_status
    if b["text"] == " ": #haven't been clicked yet
        if X_player: #true -> X's turn
            b["text"] = "X"
            X_player = False #change turn to O
            count += 1
        else: # false -> O's turn
            b["text"] = "O"
            X_player = True #change turn to X
            count += 1
    b.config(state="disabled") #disabling a clicked button
    b.config(cursor="pirate") #disabling a clicked button
    row_index = board[b][0]
    col_index = board[b][1]
    board_status[row_index][col_index] = b["text"]#updating the borad status by appending current player to place in grid
   
    if count > 4:
        check_winner(b)

#End Game function
def end_game(msg):
    disable_all_buttons()

    show_msg(msg)

def show_msg(msg):
    t = Timer(0.01,lambda: tkinter.messagebox._show("TIC TAC TOE - WINNER" , message=f"{msg}"))
    t.start()
    
    

#creating the buttons
start_label = tkinter.Label(root, text="enter board size: ")
board_size = 3
button_list =[]
button_sub_list =[]
grid_row_size = range(board_size) #[0, 1, 2]
grid_col_size = copy.copy(grid_row_size)
board = {}#dictionary -> key is button; value is grid position
board_status=[["" for index in range(board_size)] for inner_list in range(board_size)]#3x3 list that keeps track of board status 


for row in grid_row_size:
    for col in grid_col_size:
        b = Button(root, text=f" ", font=("Helvetica", 20), height=3, width=6, highlightbackground="black", cursor="spider")
        b.config(command=lambda b=b: b_click(b))#this is the most importat piece of the code!!!
        b.grid(row=row,column= col)#the gui is built here
        button_sub_list.append(b)
        board[b] = (row, col)
    button_list.append(button_sub_list)
    button_sub_list= []

    



root.mainloop()
