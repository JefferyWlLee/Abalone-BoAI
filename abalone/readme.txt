how to start the game using source code:
    step 1: ensure python 3.x is installed (was tested on 3.11.4) and added to PATH
    step 2: open terminal and navigate to where requirements.txt is located
    step 3: run the command "pip install -r requirements.txt"
    step 4: run the command "python run_game.py"

how to start game using executable:
    step 1: navigate to the folder where the executable is located
    step 2: double click the executable

How to create the executable:
    step 1: open terminal
    step 2: run pip install pyinstaller
    step 3: navigate to the folder where the source code is located
    step 4: run the command "pyinstaller --onefile --paths=/path/to/your/run_game.py run_game.py"
    step 5: navigate to the dist folder and run the executable

    Instructions on how to play the game:
    1. user will be prompted with this menu to choose the inital layout. Use arrow keys to navigate and enter to select

    example:
    [?] What type layout do you want?:
     > Standard
       German Daisy
       Belgian Daisy

     2. user will be prompted with two of the same menus to select what player will be Black and White.
        Use arrow keys to navigate and enter to select

     example:
     [?] Who do you want to be Black?:
       Player
     > Computer(Random)

     3. next the user will be prompted for the move limit, this number will be applied to both players.
        The game will end when the move limit is reached. Only ints above 0 will be accepted.

     example:
     Enter the move limit per player:

     4. Next the user will be prompted to select the time limit for each side to make a move.
        The time limit is in minutes and only ints above 0 will be accepted.
        Note, if different times are entered (i.e. 1 and 2) there is a bug that blacks time will be initially used
        for the first round, after both players have made a move, the correct times will be used with the correct time
        used up to that point.

     example:
     Enter the time limit for Black in minutes: 0.5
     Invalid input, please enter number
     Enter the time limit for Black in minutes: 1

     5. Now the game will start with this board printed to console.
     the user will be prompted with this menu.
      > In-line
       Broadside
       undo
       undo self
       pause
       resume

         a. The inline option moves marble in the direction parallel to the way thy are laid.
         This option only require choosing 1 marble

         b. The Broadside option move marbles in the direction perpendicular to the way they are laid.
         The Broadside option requires 2 marbles to be selected

         c. The undo option undoes the previous action, that is the last action the other player has made respective to
         the player who chose the undo option.

         d. The undo self option undoes the last 2 actions, that is the last action the current turn player has made.

         e. The pause option pauses the game, the game will not resume until the resume option is chosen.

         f. The resume option resumes the game if it was paused.
         if the game was not paused, the game will continue as normal.


        Example Board
        I ● ● ● ● ●
       H ● ● ● ● ● ●
      G · · ● ● ● · ·
     F · · · · · · · ·
    E · · · · · · · · ·
     D · · · · · · · · 9
      C · · ● ● ● · · 8
       B ● ● ● ● ● ● 7 <- note these are supposed to be black marbles, text files doesn't support black marbles
        A ● ● ● ● ● 6
           1 2 3 4 5

    6. once a movement option has been chosen the user will be prompted with a list of marbles
    to be selected. If the option was inline the user must choose the marble that will be
    trailing the move. If the option was broadside the user must choose the first marble,
    then will be prompted to choose a second marble. Only legal marbles will be prompted
    to be selected.

    for example if the user chose Broadside then C3 for their first marble,
    the only legal marbles to choose for the second marble would be B2, C4, and C5.

    7. next the user will be prompted to choose the direction of the move.
    only legal options will be given, for example if the user chose Broadside then C3 for their first marble,
    and C5 for their second marble, the only legal directions to choose would be North West and North East.

    inorder to choose the amount of marbles to be move in an inline move the user will have to choose the trailing marble
    for example if the user only wanted to move B2 and C3 North East, the user would choose B2 as the trailing marble
    then North East as the direction. Choosing A1 and North East will result in the same line of marbles being moved
    plus the A1 marble.

    steps 5 through 7 will be repeated until the game ends.