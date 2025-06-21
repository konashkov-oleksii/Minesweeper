import random
import tkinter as tk
field = []
chance_of_mine = 0
size_y = 16
size_x = 16
mines_count = 40
score = 0
spacing = 2
total_spacing_x = spacing * (size_x + 1)
total_spacing_y = spacing * (size_y + 1)
button_width = 40
button_height = 40
buttons = []
game_field_size_x = total_spacing_x + button_width*size_x
game_field_size_y = total_spacing_y + button_height*size_y

def create_field(size_y, size_x, mines_count):
    field.clear()
    chance_of_mine = ((size_y*size_x)/mines_count)/10
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
                
        
                   

             

    print(chance_of_mine)

create_field(size_y, size_x, mines_count)
for i in range(size_y):
    for j in range(size_x):
          print(field[i][j], end="")
    print()

def disable_button(btn, row, col):
    value = field[row][col]
    global score
    if btn['state'] == 'disabled':
        return

    if value == -1:
        btn.config(state='disabled', text='💣', bg="#974242", disabledforeground='black')
    elif value == 0:
        score += 1
        btn.config(state='disabled', text='', relief='sunken', bg='#c0c0c0')
        # Recursively reveal surrounding cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ni, nj = row + dx, col + dy
                if 0 <= ni < size_y and 0 <= nj < size_x:
                    neighbor_btn = buttons[ni][nj]
                    disable_button(neighbor_btn, ni, nj)
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
    disable_button(btn, row, col)

def right_click(event, btn):
    # Toggle flag
    if btn['state'] == 'disabled':
          return
    if btn['text'] == '🚩':
        btn.config(text='')
    else:
        btn.config(text='🚩', font=('Arial', 14, 'bold'))

def newGame():
    global field, buttons
    field = []
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
#Interface
buttons.clear()
root = tk.Tk()
root.title("Mine Field")
root.geometry('1000x1000')
frame_header = tk.Frame(root, bg="#ffffff")
frame_header.place(relheight=0.15, relwidth=0.75, relx=(1-0.75)/2, rely=0.05)
label_score = tk.Label(frame_header, text=f"Score: {score}")
label_score.pack()
btn_newGame = tk.Button(frame_header, width=10, height=3, text="New Game", command=newGame)
btn_newGame.pack()

frame_game = tk.Frame(root, bg="#5B5A5A")
frame_game.place(height=game_field_size_y, width=game_field_size_x, relx=(1-(game_field_size_x/1000))/2, rely=0.25)



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

root.mainloop()