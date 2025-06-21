import random
import tkinter as tk
field = []
game_easy = [9,9,10]
game_middle = [16,16,40]
game_hard = [30,16,99]
size_y = game_middle[0]
size_x = game_middle[1]
mines_count = game_middle[2]
mines_opened = 0
current_difficulty = []
score = 0
spacing = 2
total_spacing_x = spacing * (size_x + 1)
total_spacing_y = spacing * (size_y + 1)
button_width = 40
button_height = 40
buttons = []
game_field_size_x = total_spacing_x + button_width*size_x
game_field_size_y = total_spacing_y + button_height*size_y
mine_positions = []


def create_field(size_y, size_x, mines_count):
    field.clear()
    mines_in_field = 0
    for i in range(size_y):
        field.append([])
        for j in range(size_x):
                field[i].append("0")
            #za 0 oznacujeme pole bez miny
    while(mines_in_field < mines_count):
        x = random.randint(0, size_y-1)
        y = random.randint(0, size_x-1)
        if(field[x][y] != -1):
             field[x][y] = -1
             mine_positions.append([x, y])
             mines_in_field += 1
    for i in range(size_y):
         for j in range(size_x):
                if field[i][j] != -1:
                    mines_in_cell = 0
                    for k in range(-1,2):
                        for b in range(-1,2):
                            if(i-k<0 or i-k>=size_y):
                                  break
                            elif(j-b<0 or j-b>=size_x):
                                  continue
                            elif(field[i-k][j-b] == -1):
                                        mines_in_cell += 1
                    field[i][j] = mines_in_cell

def btn_handler_left(btn, row, col):
    value = field[row][col]
    global score, mines_opened
    if btn['state'] == 'disabled':
        return

    if value == -1:
        btn.config(state='disabled', text='💣', bg="#974242", disabledforeground='black')
        animate_explosion(btn)
        gameOver()
        return
    elif value == 0:
        score += 1
        mines_opened += 1
        btn.config(state='disabled', text='', relief='sunken', bg='#c0c0c0')
        # Recursively reveal surrounding cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ni, nj = row + dx, col + dy
                if 0 <= ni < size_y and 0 <= nj < size_x:
                    neighbor_btn = buttons[ni][nj]
                    btn_handler_left(neighbor_btn, ni, nj)
    else:
        score += 1
        color_map = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'darkblue',
            5: 'darkred',
            6: 'cyan',
            7: 'black',
            8: 'gray'
        }
        btn.config(state='disabled',
                   text=str(value),
                    disabledforeground=color_map.get(value, 'black'),
                   relief='sunken',
                   bg='#c0c0c0')
    label_score.config(text="Score:" + str(score))
def left_click(event, btn, row, col):
    if(btn['text'] == "🚩"): return
    btn_handler_left(btn, row, col)

def right_click(event, btn):
    # Toggle flag
    if btn['state'] == 'disabled':
          return
    if btn['text'] == '🚩':
        btn.config(text='')
    else:
        btn.config(text='🚩', font=('Arial', 14, 'bold'))

def newGame(difficulty):
    global size_y, size_x, mines_count, game_field_size_x, game_field_size_y, score, field,  buttons, total_spacing_x, total_spacing_y, frame_game, mine_positions, mines_opened, current_difficulty
    mines_opened = 0
    mine_positions.clear()
    size_y = difficulty[0]
    size_x = difficulty[1]
    mines_count = difficulty[2]
    current_difficulty = difficulty
    total_spacing_x = spacing * (size_x + 1)
    total_spacing_y = spacing * (size_y + 1)
    game_field_size_x = total_spacing_x + button_width*size_x
    game_field_size_y = total_spacing_y + button_height*size_y
    try: 
         frame_game.destroy()
    except:
         print("frame_game isnt here")
    frame_game = tk.Frame(root, bg="#5B5A5A")
    frame_game.place(height=game_field_size_y, width=game_field_size_x, relx=(1-(game_field_size_x/1000))/2, rely=0.25)
    
    field.clear()
    for row_buttons in buttons:
        for btn in row_buttons:
            btn.destroy()
    buttons.clear()
    create_field(size_y, size_x, mines_count)
    for row in range(size_y):
        row_buttons = []
        for col in range(size_x):
            btn = tk.Button(frame_game, width=10, height=3)
            x_pos = spacing + col * (button_width + spacing)
            y_pos = spacing + row * (button_height + spacing)
            btn.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
            btn.bind('<Button-1>', lambda e, b=btn, r=row, c=col: left_click(e, b, r, c))
            btn.bind('<Button-3>', lambda e, b=btn: right_click(e, b))
            row_buttons.append(btn)
        buttons.append(row_buttons)


def gameOver():
    global buttons, mine_positions
    for row in buttons:
         for btn in row:
              btn.config(state = "disabled")
    for mine in mine_positions:
         animate_explosion(buttons[mine[0]][mine[1]])

def animate_explosion(btn, delay=100):
    btn.config(text='💣', bg="#974242", disabledforeground='black')
    btn.after(200, lambda: btn.config(text='💥', bg="#000000", fg="white"))

def gameWon():
     return
#Interface
buttons.clear()
root = tk.Tk()
root.title("Mine Field")
root.geometry(f'{max(1000, game_field_size_x + 100)}x{max(1000, game_field_size_y + 200)}')
frame_header = tk.Frame(root)
frame_header.place(relheight=0.15, relwidth=0.75, relx=(1-0.75)/2, rely=0.05)

label_score = tk.Label(frame_header, text=f"Score: {score}")
label_score.pack(side="top", anchor="n")

label_result = tk.Label(frame_header)
label_result.pack(anchor="center", side="bottom")
bottom_button_frame = tk.Frame(frame_header)
bottom_button_frame.pack(side="bottom", pady=10)

btn_easy = tk.Button(bottom_button_frame, text="Easy", width=10, height=2, command=lambda: newGame(game_easy))
btn_easy.pack(side="left", padx=5)

btn_medium = tk.Button(bottom_button_frame, text="Medium", width=10, height=2, command=lambda: newGame(game_middle))
btn_medium.pack(side="left", padx=5)

#btn_hard = tk.Button(bottom_button_frame, text="Hard", width=10, height=2, command=lambda: newGame(game_hard))
#btn_hard.pack(side="left", padx=5)
newGame(game_middle)

root.mainloop()