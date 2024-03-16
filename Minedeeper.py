from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import sys
import pyautogui as pg
from functools import partial
import time
import threading
import BoardExtractor as be
import ProbabilityComputer as pc

def displayBoard(msBoard, start_time):        
    def timer(time_label, counter):
        time_label.configure(text=f"Time: {msBoard.time + counter}")
        time_label.after(1000, partial(timer, time_label, counter + 1))
                    
    def activateProbability():
        def probabilityTasks():
            def analyzingAnimation(counter):
                if state == "Analyzed":
                    return
                
                if not hasattr(analyzingAnimation, "currentState"):
                    analyzingAnimation.currentState = state
                elif analyzingAnimation.currentState != state:
                    analyzingAnimation.currentState = state
                    counter = 0
                
                analyze_radio_button.configure(text=state + ' .' * counter)
                analyze_radio_button.after(1000, partial(analyzingAnimation, counter + 1 if counter < 3 else 0))
                
            state = "Analyzing"
                        
            analyze_radio_button.configure(text=state,
                                           fg_color=cell_background_colors["MINE"],
                                           state=ctk.DISABLED)
            
            analyze_radio_button.grid(row=msBoard.size[0]-5 if msBoard.size[0] >= 12 else msBoard.size[0] + 1 if msBoard.size[0] >= 6 else 7,
                                      column=0, columnspan=2, sticky='we', padx=10)            
            hint_checkbox.grid_forget()
            
            analyzingAnimation(counter=0)
            
            for processingState in pc.computeProbability(board=msBoard.board, size=msBoard.size, total_mines=msBoard.total_mines, guessLocation=displayBoard.guess_location):
                state = processingState
                analyze_radio_button.configure(text=state)
                
            if displayBoard.guessed_location is not None:
                buttons[displayBoard.guessed_location[0] * msBoard.size[1] + displayBoard.guessed_location[1]].configure(fg_color=cell_background_colors["CLOSED"])
                
            displayBoard.guessed_location = displayBoard.guess_location
                
            discovered_mines = pc.countDiscoveredMines(msBoard.board)
            
            discovered_mines_label.configure(text=f"Discovered mines: {discovered_mines}")
            remaining_mines_label.configure(text=f"Remaining mines: {msBoard.total_mines - discovered_mines}")
            safe_cells_label.configure(text=f"Unopened safe cells: {pc.countUnopenedSafeCells(msBoard.board)}")
            
            if displayBoard.guessed_location is not None:
                buttons[displayBoard.guessed_location[0] * msBoard.size[1] + displayBoard.guessed_location[1]].configure(text='', fg_color=cell_background_colors["GUESSED"])            
            analyze_radio_button.configure(fg_color=cell_background_colors["SAFE"],
                                           text_color_disabled=cell_text_colors["ENABLED"],
                                           width=0)
            hint_checkbox.configure(state=ctk.NORMAL)
            probability_options_button.configure(state=ctk.NORMAL)
            
            if probability_options_button.get() == '':
                probability_options_button.set("Off")
            
            analyze_radio_button.grid(row=msBoard.size[0]-5 if msBoard.size[0] >= 12 else msBoard.size[0] + 1 if msBoard.size[0] >= 6 else 7,
                                      column=0, columnspan=1, sticky='we', padx=10)            
            hint_checkbox.grid(row=msBoard.size[0]-5 if msBoard.size[0] >= 12 else msBoard.size[0] + 1 if msBoard.size[0] >= 6 else 7,
                               column=1)
            
            hypothesisMode(mode=hypothesis_options_button.get())
            probabilityMode(mode=probability_options_button.get())
            if hint_checkbox.get() == 1:
                hintMode()
        
        activateProbabilityThread = threading.Thread(target=probabilityTasks)
        activateProbabilityThread.start()
                    
    def hintMode():
        if hint_checkbox.get() == 1:
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if msBoard.board[i][j].probability == -1:
                        continue
                    if msBoard.board[i][j].type == -2 and msBoard.board[i][j].probability != 100:
                        buttons[i * msBoard.size[1] + j].configure(fg_color=cell_background_colors["WARNING"])
                    elif msBoard.board[i][j].probability == 0:
                        buttons[i * msBoard.size[1] + j].configure(fg_color=cell_background_colors["SAFE"])
                    elif msBoard.board[i][j].probability == 100:
                        buttons[i * msBoard.size[1] + j].configure(fg_color=cell_background_colors["MINE"])
                    elif not msBoard.board[i][j].open:
                        buttons[i * msBoard.size[1] + j].configure(fg_color=cell_background_colors["CLOSED"])
        else:
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if not msBoard.board[i][j].open:
                        buttons[i * msBoard.size[1] + j].configure(fg_color=cell_background_colors["CLOSED"])
        
    def hypothesisMode(mode):
        if mode == "Display":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if msBoard.board[i][j].type == -2:
                        buttons[i * msBoard.size[1] + j].configure(text="")
                        buttons[i * msBoard.size[1] + j].configure(state=ctk.NORMAL,
                                                                image=flag_image if msBoard.board[i][j].type == -2 else None)
                        buttons[i * msBoard.size[1] + j]._draw()
        elif mode == "Lock":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if not msBoard.board[i][j].open or msBoard.board[i][j].type == 9:
                        buttons[i * msBoard.size[1] + j].configure(state=ctk.DISABLED)
        elif mode == "Flag":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if not msBoard.board[i][j].open or msBoard.board[i][j].type == 9:
                        buttons[i * msBoard.size[1] + j].configure(state=ctk.NORMAL, command=partial(switchCellType, i, j, mode))  
        elif mode == "Guess":
            if pc.isComputed(guessLocation=None):
                for i in range(msBoard.size[0]):
                    for j in range(msBoard.size[1]):
                        if not msBoard.board[i][j].open or msBoard.board[i][j].type == 9:
                            buttons[i * msBoard.size[1] + j].configure(state=ctk.NORMAL, command=partial(switchCellType, i, j, mode))
            else:
                for i in range(msBoard.size[0]):
                    for j in range(msBoard.size[1]):
                        if not msBoard.board[i][j].open or msBoard.board[i][j].type == 9:
                            buttons[i * msBoard.size[1] + j].configure(state=ctk.DISABLED)
                
                messagebox.showwarning("Warning",
                                "Not Available Option!\nPlease analyze the board before guessing.",
                                icon='warning')                  
                    
    def probabilityMode(mode):
        if mode == "Off":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if displayBoard.guess_location != displayBoard.guessed_location and i == displayBoard.guess_location[0] and j == displayBoard.guess_location[1]:
                        buttons[i * msBoard.size[1] + j].configure(text='')  
                    elif not msBoard.board[i][j].open:
                        buttons[i * msBoard.size[1] + j].configure(text='')
        elif mode == "Edge":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if displayBoard.guess_location != displayBoard.guessed_location and displayBoard.guess_location is not None and i == displayBoard.guess_location[0] and j == displayBoard.guess_location[1]:
                        buttons[i * msBoard.size[1] + j].configure(text=msBoard.board[i][j].probability)                        
                    elif (not msBoard.board[i][j].open and msBoard.board[i][j].edge) or (msBoard.board[i][j].probability == 0 or msBoard.board[i][j].probability == 100):
                        buttons[i * msBoard.size[1] + j].configure(text=msBoard.board[i][j].probability if msBoard.board[i][j].type != -2 else '')
                    elif not msBoard.board[i][j].open:
                        buttons[i * msBoard.size[1] + j].configure(text='')
        elif mode == "All":
            for i in range(msBoard.size[0]):
                for j in range(msBoard.size[1]):
                    if displayBoard.guess_location != displayBoard.guessed_location and i == displayBoard.guess_location[0] and j == displayBoard.guess_location[1]:
                        buttons[i * msBoard.size[1] + j].configure(text=msBoard.board[i][j].probability)  
                    elif not msBoard.board[i][j].open:
                        buttons[i * msBoard.size[1] + j].configure(text=msBoard.board[i][j].probability if msBoard.board[i][j].type != -2 else '')
                    
    def switchMode(mode):
        if mode == "Hypothesis":
            probability_options_button.grid_forget()
            hypothesis_options_button.grid(row=msBoard.size[0]-4 if msBoard.size[0] >= 12 else msBoard.size[0] + 2 if msBoard.size[0] >= 6 else 8,
                                           column=0, columnspan=2,
                                           sticky='we')
            hypothesisMode(mode="Display")
        elif mode == "Probability":
            hypothesis_options_button.grid_forget()
            probability_options_button.grid(row=msBoard.size[0]-4 if msBoard.size[0] >= 12 else msBoard.size[0] + 2 if msBoard.size[0] >= 6 else 8,
                                            column=0, columnspan=2,
                                            sticky='we')
            
            probabilityMode(mode=probability_options_button.get())
        
    def showOriginalBoard():
        originalBoardThread = threading.Thread(target=be.visualizeBoard, args=[msBoard, displayBoard.guessed_location, hint_checkbox.get()])
        originalBoardThread.start()
        
    def recapture():
        try:
            start_time = time.perf_counter()
            
            board_image = pg.screenshot()
            msBoard = be.getBoardInfo(input=board_image, isScreenshot=True)
            
            pc.clearComputedBoards()
            
            root.destroy()
            displayBoard(msBoard=msBoard, start_time=start_time)
        except Exception as e:
            messagebox.showerror("Error",
                                "Board Error!\nPlease make the board visible on screen before capture.\nYou can return to main menu for smaller window.",
                                icon='error')
        
    def returnMainMenu():
        root.destroy()
        mainMenu()
            
    def close():
        root.destroy()
        sys.exit()
            
    def switchCellType(row, col, mode):
        if mode == "Flag":
            if msBoard.board[row][col].type == -1:
                msBoard.board[row][col].type = -2
                msBoard.total_flags += 1
                buttons[row * msBoard.size[1] + col].configure(text="")
                buttons[row * msBoard.size[1] + col].configure(image=flag_image)
                buttons[row * msBoard.size[1] + col]._draw()
                if hint_checkbox.get() == 1:
                    if msBoard.board[row][col].probability != 100:
                        buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["WARNING"])
            elif msBoard.board[row][col].type == -2:
                msBoard.board[row][col].type = -1
                msBoard.total_flags -= 1
                buttons[row * msBoard.size[1] + col].configure(image=None)
                buttons[row * msBoard.size[1] + col]._draw()
                if probability_options_button.get() == "Off":
                    buttons[row * msBoard.size[1] + col].configure(text="")
                elif probability_options_button.get() == "Edge":
                    if msBoard.board[row][col].edge or msBoard.board[row][col].probability == 0 or msBoard.board[row][col].probability == 100:
                        buttons[row * msBoard.size[1] + col].configure(text=msBoard.board[row][col].probability)
                    else:
                        buttons[row * msBoard.size[1] + col].configure(text='')
                elif probability_options_button.get() == "All":                    
                    buttons[row * msBoard.size[1] + col].configure(text=msBoard.board[row][col].probability if msBoard.board[row][col].probability >= 0 else "")
                if hint_checkbox.get() == 1:
                    if msBoard.board[row][col].probability == 0:
                        buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["SAFE"])
                    elif msBoard.board[row][col].probability == 100:
                        buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["MINE"])
                    else:
                        buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["CLOSED"])
                
            total_flags_label.configure(text=f"Total flags: {msBoard.total_flags}")
        
        elif mode == 'Guess':
            if not msBoard.board[row][col].guessing:
                return
            
            if msBoard.board[row][col].type == -1:
                if displayBoard.guess_location is not None:
                    msBoard.board[displayBoard.guess_location[0]][displayBoard.guess_location[1]].type = -1
                    msBoard.board[displayBoard.guess_location[0]][displayBoard.guess_location[1]].open = False
                    if displayBoard.guess_location != displayBoard.guessed_location:
                        if hint_checkbox.get() == 1:
                            if msBoard.board[displayBoard.guess_location[0]][displayBoard.guess_location[1]].probability == 0:
                                buttons[displayBoard.guess_location[0] * msBoard.size[1] + displayBoard.guess_location[1]].configure(fg_color=cell_background_colors["SAFE"])
                            elif msBoard.board[displayBoard.guess_location[0]][displayBoard.guess_location[1]].probability == 100:
                                buttons[displayBoard.guess_location[0] * msBoard.size[1] + displayBoard.guess_location[1]].configure(fg_color=cell_background_colors["MINE"])
                            else:
                                buttons[displayBoard.guess_location[0] * msBoard.size[1] + displayBoard.guess_location[1]].configure(fg_color=cell_background_colors["CLOSED"])
                        else:
                            buttons[displayBoard.guess_location[0] * msBoard.size[1] + displayBoard.guess_location[1]].configure(fg_color=cell_background_colors["CLOSED"])
                    else:
                        buttons[displayBoard.guess_location[0] * msBoard.size[1] + displayBoard.guess_location[1]].configure(fg_color=cell_background_colors["DEAD"])
                
                displayBoard.guess_location = (row, col)
                
                msBoard.board[row][col].type = 9
                msBoard.board[row][col].open = True
                
                if displayBoard.guess_location != displayBoard.guessed_location:
                    buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["GUESS"])
                else:
                    buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["GUESSED"])
                    
            elif msBoard.board[row][col].type == 9:
                displayBoard.guess_location = None
                
                msBoard.board[row][col].type = -1
                msBoard.board[row][col].open = False
                
                if (row, col) != displayBoard.guessed_location:
                    if hint_checkbox.get() == 1:
                        if msBoard.board[row][col].probability == 0:
                            buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["SAFE"])
                        elif msBoard.board[row][col].probability == 100:
                            buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["MINE"])
                        else:
                            buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["CLOSED"])
                    else:
                        buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["CLOSED"])
                else:
                    buttons[row * msBoard.size[1] + col].configure(fg_color=cell_background_colors["DEAD"])
                
            if displayBoard.guessed_location == displayBoard.guess_location and pc.isComputed(guessLocation=displayBoard.guess_location):
                analyze_radio_button.configure(text="Analyzed",
                                               fg_color=cell_background_colors["SAFE"],
                                               text_color_disabled=cell_text_colors["ENABLED"],
                                               state=ctk.DISABLED)
                analyze_radio_button.select()
            else:
                analyze_radio_button.configure(text="Analyze",
                                               text_color=cell_background_colors["CLOSED"],
                                               text_color_disabled=cell_background_colors["CLOSED"],
                                               fg_color=cell_background_colors["MINE"],
                                               state=ctk.NORMAL)
                analyze_radio_button.deselect()
                
    
    # Assets
    flag_image = ctk.CTkImage(light_image=Image.open("assets/minedeeper/flag.png"),
                              dark_image=Image.open("assets/minedeeper/flag.png"),
                              size=(20, 20))
    
    cell_background_colors = {
        "OPENED": "#c4c4c4",
        "GUESS": "#459ef7",
        "GUESSED": "#4faed6",
        "CLOSED": "#848484",
        "SAFE": "#37b35c",
        "SAFEHOVER": "#4ecc73",
        "MINE": "#c4101f",
        "WARNING": "#f7df07",
        "HOVER": "#84ecfa",
        "DEAD": "#3c4d96"
    }
    
    cell_text_colors = {
        "DISABLED": "#4f3838",
        "ENABLED": "#ffffff",
        -2: "#000000",
        -1: "#000000",
        0: "#c4c4c4",
        1: "#0505fb",
        2: "#068406",
        3: "#fb0707",
        4: "#050584",
        5: "#850909",
        6: "#048484",
        7: "#050505",
        8: "#848484"
    }
    
    displayBoard.guess_location = None
    displayBoard.guessed_location = None

    # Create a new main window
    root = ctk.CTk()
    root.title("Minedeeper")
    root.iconbitmap('assets/minedeeper_icon.ico')

    # Create a label widget
    analyzer_label = ctk.CTkLabel(root, text="Analyzer", width=220)
    analyzer_label.grid(row=0, column=0, pady=10, columnspan=2)
    
    if msBoard.time is not None:
        msBoard.time = int(msBoard.time + time.perf_counter() - start_time)
        time_label = ctk.CTkLabel(root, text=f"Time: {msBoard.time}")
        time_label.grid(row=1, column=0, columnspan=2)
        
        timer(time_label=time_label, counter=0)
    else:
        time_label = ctk.CTkLabel(root, text=f"Time: Not available")
        time_label.grid(row=1, column=0, columnspan=2)
    
    total_mines_label = ctk.CTkLabel(root, text=f"Total mines: {msBoard.total_mines}")
    total_mines_label.grid(row=2, column=0, columnspan=2)
    
    total_flags_label = ctk.CTkLabel(root, text=f"Total flags: {msBoard.total_flags}")
    total_flags_label.grid(row=3, column=0, columnspan=2)
    
    discovered_mines_label = ctk.CTkLabel(root, text=f"Discovered mines: Unknown")
    discovered_mines_label.grid(row=4, column=0, columnspan=2)
    
    remaining_mines_label = ctk.CTkLabel(root, text=f"Remaining mines: Unknown")
    remaining_mines_label.grid(row=5, column=0, columnspan=2)
    
    safe_cells_label = ctk.CTkLabel(root, text=f"Unopened safe cells: Unknown")
    safe_cells_label.grid(row=6, column=0, columnspan=2)
            
    # Probability Radio Button
    analyze_radio_button = ctk.CTkRadioButton(root,
                                           text="Analyze",
                                           text_color=cell_background_colors["CLOSED"],
                                           text_color_disabled=cell_background_colors["CLOSED"],
                                           fg_color=cell_background_colors["MINE"],
                                           command=activateProbability,
                                           width=0)
    analyze_radio_button.grid(row=msBoard.size[0]-5 if msBoard.size[0] >= 12 else msBoard.size[0] + 1 if msBoard.size[0] >= 6 else 7,
                           column=0, sticky='we', padx=10)
            
    # Hint Checkbox
    hint_checkbox = ctk.CTkCheckBox(root,
                                  text="Hint",
                                  text_color_disabled=cell_background_colors["CLOSED"],
                                  fg_color=cell_background_colors["SAFE"],
                                  state=ctk.DISABLED,
                                  command=hintMode,
                                  width=0)
    hint_checkbox.grid(row=msBoard.size[0]-5 if msBoard.size[0] >= 12 else msBoard.size[0] + 1 if msBoard.size[0] >= 6 else 7,
                     column=1)
    
    # Hypothesis Options Segmented Button
    hypothesis_options = ["Flag", "Guess", "Lock"]
    hypothesis_options_button = ctk.CTkSegmentedButton(root,
                                                       values=hypothesis_options,                                        
                                                       selected_color=cell_background_colors["SAFE"],
                                                       selected_hover_color=cell_background_colors["SAFEHOVER"],
                                                       command=hypothesisMode)
    hypothesis_options_button.set("Flag")
    hypothesis_options_button.grid(row=msBoard.size[0]-4 if msBoard.size[0] >= 12 else msBoard.size[0] + 2 if msBoard.size[0] >= 6 else 8,
                                 column=0, columnspan=2,
                                 sticky='we')
    
    # Probability Options Segmented Button
    probability_options = ["Off", "Edge", "All"]
    probability_options_button = ctk.CTkSegmentedButton(root,
                                                        values=probability_options,
                                                        selected_color=cell_background_colors["SAFE"],
                                                        selected_hover_color=cell_background_colors["SAFEHOVER"],
                                                        state=ctk.DISABLED,
                                                        command=probabilityMode)
    
    # Mode Options Button
    mode_options = ["Hypothesis", "Probability"]
    mode_options_button = ctk.CTkSegmentedButton(root,
                                                 values=mode_options,
                                                 selected_color=cell_background_colors["SAFE"],
                                                 selected_hover_color=cell_background_colors["SAFEHOVER"],
                                                 command=switchMode)
    mode_options_button.set("Hypothesis")
    mode_options_button.grid(row=msBoard.size[0]-3 if msBoard.size[0] >= 12 else msBoard.size[0] + 3 if msBoard.size[0] >= 6 else 9,
                          column=0,
                          columnspan=2,
                          sticky='we')
    
    # Original Board Button      
    original_board_button = ctk.CTkButton(root,
                                          text="Original Board",
                                          fg_color=cell_background_colors["GUESS"],
                                          command=showOriginalBoard)
    original_board_button.grid(row=msBoard.size[0]-2 if msBoard.size[0] >= 12 else msBoard.size[0] + 4 if msBoard.size[0] >= 6 else 10,
                               column=0,
                               columnspan=2,
                               sticky='we')

    # Recapture Button
    recapture_button = ctk.CTkButton(root, text="Re-Capture", command=recapture)
    recapture_button.grid(row=msBoard.size[0]-1 if msBoard.size[0] >= 12 else msBoard.size[0] + 5 if msBoard.size[0] >= 6 else 11,
                          column=0,
                          columnspan=2,
                          sticky='we')

    # Menu Button
    menu_button = ctk.CTkButton(root, text="Main Menu", command=returnMainMenu)
    menu_button.grid(row=msBoard.size[0] if msBoard.size[0] >= 12 else msBoard.size[0] + 6 if msBoard.size[0] >= 6 else 12,
                     column=0,
                     columnspan=2,
                     sticky='we')
    
    header_label = ctk.CTkLabel(root, text="MINEDEEPER")
    header_label.grid(row=0, column=2, columnspan=msBoard.size[1], pady=10)
    
    buttons = []
    for i in range(msBoard.size[0]):
        for j in range(msBoard.size[1]):
            button = ctk.CTkButton(
                root,
                image=flag_image if msBoard.board[i][j].type == -2 else None,
                font=ctk.CTkFont(family="Helvetica", size=20, weight="bold") if msBoard.board[i][j].type > 0 else ctk.CTkFont(family="Helvetica", size=14),
                text=str(msBoard.board[i][j].type) if msBoard.board[i][j].type > 0 else "",
                state=ctk.DISABLED if msBoard.board[i][j].type >= 0 else ctk.NORMAL,
                width=30,  # Adjust the width as needed
                height=30,  # Adjust the height as needed
                border_width=1,
                border_spacing=0,
                corner_radius=0,
                text_color=cell_text_colors[msBoard.board[i][j].type],
                text_color_disabled=cell_text_colors[msBoard.board[i][j].type],
                fg_color=cell_background_colors["CLOSED"] if msBoard.board[i][j].type < 0 else cell_background_colors["OPENED"],
                hover_color=cell_background_colors["HOVER"],
                command=partial(switchCellType, i, j, hypothesis_options_button.get())
            )
            buttons.append(button)
            button.grid(row=i+1, column=j+2, padx=0, pady=0)

    root.protocol("WM_DELETE_WINDOW", close)
    # Start the Tkinter event loop
    root.mainloop()

def mainMenu(isFirstRun=False):    
    def captureBoard():
        try:
            start_time = time.perf_counter()
            
            board_image = pg.screenshot()
            msBoard = be.getBoardInfo(input=board_image, isScreenshot=True)
            
            pc.clearComputedBoards()
                    
            root.destroy()
            displayBoard(msBoard=msBoard, start_time=start_time)
        except Exception as e:
            messagebox.showerror("Error",
                                "Board Error!\nPlease make the board visible on screen before capture.",
                                icon='error')
    
    def on_closing():
    # This function will be called when the window is closed
        root.destroy()
        sys.exit()

    # Create the main application window
    root = ctk.CTk()
    root.title("Minedeeper")
    root.iconbitmap('assets/minedeeper_icon.ico')

    # Set window size
    window_width = 235
    window_height = 125
    root.geometry(f"{window_width}x{window_height}")

    # Place the window in the center of the screen
    if isFirstRun:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"+{x}+{y}")
    
    # Header
    header_label = ctk.CTkLabel(
        root, text="MINEDEEPER")
    header_label.pack(pady=10)

    # Create button
    capture_button = ctk.CTkButton(root, text="CAPTURE", command=captureBoard)
    capture_button.pack()

    # Create info label
    info_label = ctk.CTkLabel(root, text="Screenshot and Analyze")
    info_label.pack(pady=10)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the Tkinter event loop
    root.mainloop()
    


mainMenu(isFirstRun=True)