import os
from abc import ABC , abstractmethod
import copy
import random
import time

class Board:
    __slot__ = ["__BOARD" , "__dim" , "__CELL_INDEXES_MAP" , "__INDEXES_CELL_MAP" , "__winning_conditions"]

    def __init__(self , n):
        self.__dim = n
        board = []
        c = []
        for number in range(1,n**2 + 1):
            c.append(number)
            if number % n == 0:
                board.append(c)
                c = []
        board.reverse()
        self.__BOARD = board
        self.Cell_Index_Cell()
        self.find_winning_conditions()

    @property 
    def BOARD(self):
        return self.__BOARD
    @property 
    def dim(self):
        return self.__dim
    
    @BOARD.setter 
    def BOARD(self , List : list):
        self.__BOARD = List
    

    def display(self):
        os.system("cls")
        print(f"{"Board":-^{self.dim * 7 - 5}}" , "\n")
        for row in self.BOARD:
            for cell in row:
                print(f"{cell:^5}" , end = "|")
            print("\b \n")

    def Cell_Index_Cell(self):
        dic = dict()
        for i in range(self.dim):
            for j in range(self.dim):
                dic[self.BOARD[i][j]] = (i,j)
        self.__CELL_INDEXES_MAP = dic

        dic = dict()
        for i in range(self.dim):
            for j in range(self.dim):
                dic[(i,j)] = self.BOARD[i][j]
        self.__INDEXES_CELL_MAP = dic

    @property
    def Index_Cell_Map(self):
        return self.__INDEXES_CELL_MAP
    @property
    def Cell_Index_Map(self):
        return self.__CELL_INDEXES_MAP
    
    def find_winning_conditions(self):
        # سطرها 
        win = []
        for row in self.BOARD:
            win.append(tuple(row))
        # ستون ها
        c = []
        for i in range(self.dim):
            for j in range(self.dim):
                c.append(self.BOARD[j][i])
            win.append(tuple(c))
            c = []
        # قطر ها
        c1 = []
        for i in range(self.dim):
            for j in range(self.dim):
                 if i == j:
                     c1.append(self.BOARD[i][j])
        win.append(tuple(c1))

        c2 = []
        for tpl in self.Index_Cell_Map:
            if tpl[0] + tpl[1] == self.dim - 1:
                c2.append(self.Index_Cell_Map.get(tpl))
        win.append(tuple(c2))

        self.__winning_conditions = win


    @property
    def winning_conditions(self):
        return self.__winning_conditions
    

    def read_board(self , cell):
        if cell in range(1,self.dim ** 2 + 1):
            i , j = self.Cell_Index_Map[cell]
            return self.BOARD[i][j]
        return None
        

    def check_winner(self , board = None):
        if board == None:
            board = self.BOARD
        for winning_condition in self.winning_conditions :
            cell_mark = []
            for cell in winning_condition:
                i , j = self.Cell_Index_Map[cell]
                cell_mark.append(board[i][j])
            if len(set(cell_mark)) == 1:
                return cell_mark[0]
        return False

    def get_empty_cells(self):
        empty = []
        for row in self.BOARD:
            for cell in row:
                if isinstance(cell , int):
                    empty.append(cell)
        return empty


    def find_next_cell_to_win(self, mark):
        temp = copy.deepcopy(self.BOARD)
        empty = self.get_empty_cells()
        for empty_cell in empty:
            i , j = self.Cell_Index_Map[empty_cell]
            temp[i][j] = mark
            if  self.check_winner(temp):
                return empty_cell
            else:
                temp = copy.deepcopy(self.BOARD)
        return False

    def check_has_board_empty_cell(self):
        return any([any([isinstance(cell , int) for cell in row]) for row in self.BOARD])

class Player(ABC):
    __slot__ = ["__mark"]        

    @abstractmethod
    def choose(self):
        pass

class HumanPlayer(Player):
    
    def __init__(self , mark ):
        self.__mark = mark
    
    def choose(self , board : Board):
        empty = board.get_empty_cells()
        choice = int(input("Enter Cell , '0' for Save and Exit : "))
        while choice != 0 and choice not in empty:
            print("Wrong choice!")
            choice = int(input("Enter Cell , '0' for Save and Exit : "))
        if choice == 0:
            return "SAVE"
        else:
            i , j = board.Cell_Index_Map[choice]
            board.BOARD[i][j] = self.__mark
    @property
    def mark(self):
        return self.__mark
    
class CPUPlayer(Player):
    __slots__ = ["__level"]
    def __init__(self , mark , level):
        self.__mark = mark
        match level:
            case 1: self.__level = "Easy"
            case 2: self.__level = "Medium"
            case 3: self.__level = "Hard"
    
    def find_player_mark(self):
        if self.__mark == "X":
            return "O"
        return "X"
    def choose_random_from_empty(self , board : Board):
        empty = board.get_empty_cells()
        return random.sample(empty , k = 1)[0]
    
    def choose(self, board : Board):
        time.sleep(0.5)
        choice = None
        
        match self.__level:
            case "Easy": 
                a = self.choose_random_from_empty(board)
            case "Medium" : 
                a = board.find_next_cell_to_win(self.find_player_mark()) or self.choose_random_from_empty(board)
            case "Hard" :
                a = board.find_next_cell_to_win(self.__mark) or board.find_next_cell_to_win(self.find_player_mark()) or self.choose_random_from_empty(board)
        i , j = board.Cell_Index_Map[a]
        board.BOARD[i][j] = self.__mark

    
    @property
    def mark(self):
        return self.__mark

        
    
class GameSetting:
    __slots__ = ["__Board" , "__Board_dim" , "__Players" , "__Turn_Mark" , "__Single_User_Mark" , "__Game_mode" , "__CPU_Level"]

    Marks = ("X" , "O")

    def __init__(self , packed_setting = None):
        if packed_setting == None:
            self.__Board = ""
            self.__Board_dim = 2
            self.__Players = []
            self.__Turn_Mark = ""
            self.__Single_User_Mark = ""
            self.__Game_mode = ""
            self.__CPU_Level = 0
        else:
            # {'self.__Board': '', 'self.__Board_dim': 2, 'self.__Players': [], 'self.__Turn_Mark': '', 'self.__Single_User_Mark': '', 'self.__Game_mode': '', 'self.__CPU_Level': 0}
            setting_values = packed_setting.values()
            self.__Board, self.__Board_dim, self.__Players, self.__Turn_Mark, self.__Single_User_Mark, self.__Game_mode, self.__CPU_Level = setting_values

    def get_story(self):
        os.system('cls')
        print('Main Menu\n---------')
        print('1- New Game\n2- Resume Previous Game')

        choice = input("Enter Story: ")
        while choice not in ("1" , "2"):
            print("Wrong Choice !")
            choice = input("Enter Story: ")
        
        return "new" if choice == "1" else "resume"
    
    def get_mode(self):
        os.system('cls')
        print('Mode Setting\n------------')
        print('1- Single Player\n2- Multi Player')

        choice = input('Enter mode: ')
        while choice not in ('1', '2'):
            print('Wrong choice!')
            choice = input('Enter mode: ')

        self.__Game_mode = 'single' if choice == '1' else 'multi'
    

    def get_cpu_level(self):
        os.system('cls')
        print('CPU Setting\n-----------')
        print('1- Easy\n2- Medium\n3- Hard')

        choice = input('Enter level: ')
        while choice not in ('1', '2', '3'):
            print('Wrong choice!')
            choice = input('Enter level: ')

        match choice:
            case '1':
                self.__CPU_Level =  ('easy' , 1)
            case '2':
                self.__CPU_Level =  ('medium' , 2)
            case '3':
                self.__CPU_Level =  ('hard', 3)
    
    
    def get_board_dim(self):
        os.system('cls')
        print('Board Setting\n-----------')
    
        choice = input("Enter Dimentional of Board (n*n) : ")
        while not choice.isdigit() or int(choice) <= 0 :
            print('Wrong choice!')
            choice = input("Enter Dimentional of Board (n*n) : ")
        
        self.__Board_dim = int(choice)

    def construct_board(self):
        self.__Board = Board(self.__Board_dim)
    
    def get_single_user_mark(self):
        os.system('cls')
        print('SINGLE PLAYER Setting\n---------------------')

        self.__Single_User_Mark = input('Choose your mark between "X" and "O": ').upper()
        while self.__Single_User_Mark not in self.Marks:
            print('Wrong mark!')
            self.__Single_User_Mark = input('Choose your mark between "X" and "O": ').upper()


    def update_turn(self):
        if not self.__Turn_Mark:
            self.__Turn_Mark = random.sample(['X', 'O'], k=1)[0]
        else:
            if self.__Turn_Mark == 'X':
                self.__Turn_Mark = 'O'
            else:
                self.__Turn_Mark = 'X'

    def construct_players(self):
        match self.__Game_mode:
            case "single":
                cpu_mark = "O" if self.__Single_User_Mark == "X" else "X" 
                self.__Players = [HumanPlayer(self.__Single_User_Mark ) , CPUPlayer(cpu_mark , self.__CPU_Level[1])]
            case "multi":
                mark1 , mark2 = random.sample(["X" , "O"], k = 2)
                self.__Players = [HumanPlayer(mark1) , HumanPlayer(mark2)]
        

    def pack_settings(self):
        settings = {
        "self.__Board" : self.__Board.BOARD,
        "self.__Board_dim" : self.__Board_dim,
        "self.__Players" : [self.__Players[0].mark , self.__Players[1].mark],
        "self.__Turn_Mark" : self.__Turn_Mark,
        "self.__Single_User_Mark" : self.__Single_User_Mark,
        "self.__Game_mode" : self.__Game_mode,
        "self.__CPU_Level" : self.__CPU_Level,
        }
        return settings
    
    
    @property
    def Game_mode(self):
        return self.__Game_mode
    
    @property
    def Board(self):
        return self.__Board
    
    @property
    def Turn_Mark(self):
        return self.__Turn_Mark
    


    def get_turner_cell(self):
            print(f'{self.__Turn_Mark} turn.')
            pl = self.__Players
            if pl[0].mark == self.__Turn_Mark:
                ch = pl[0].choose(self.__Board)
                if ch == "SAVE":
                    return "SAVE"
            else:
                ch = pl[1].choose(self.__Board)
                if ch == "SAVE":
                    return "SAVE"

    @property
    def Single_User_Mark(self):
        return self.__Single_User_Mark
    
    now_object = None

    @classmethod
    def make_object_from_now_setting(cls):
        return cls


    


class GameManager:
    __slots_ = ["__Game_Setting_Object" , "__Save_Load_Object"]

    def __init__(self , Setting_object = None):
        if  Setting_object == None:
            self.__Game_Setting_Object = GameSetting()
            self.__Save_Load_Object = Load_Save()
        else:
            self.__Game_Setting_Object = Setting_object
            self.__Save_Load_Object = Load_Save()

    
    @property 
    def Game_Setting_Object(self):
        return self.__Game_Setting_Object
    
    def setup_game(self):
        story = self.Game_Setting_Object.get_story()
        if story == 'new':
            self.Game_Setting_Object.get_mode()
            if self.__Game_Setting_Object.Game_mode == 'single':
                self.Game_Setting_Object.get_cpu_level()
                self.Game_Setting_Object.get_board_dim()
                self.Game_Setting_Object.get_single_user_mark()
                self.Game_Setting_Object.construct_board()
                self.Game_Setting_Object.construct_players()
                self.Game_Setting_Object.update_turn()
            else: # MODE == 'multi':
                self.Game_Setting_Object.get_board_dim()
                self.Game_Setting_Object.construct_board()
                self.Game_Setting_Object.construct_players()
                self.Game_Setting_Object.update_turn()
        else: # story == 'resume':
            loaded_version = self.__Save_Load_Object.load_game()
            self.__Game_Setting_Object = loaded_version
    
    def run_game(self):
        while self.Game_Setting_Object.Board.check_has_board_empty_cell() and not self.Game_Setting_Object.Board.check_winner():
            self.Game_Setting_Object.Board.display()
            ch = self.Game_Setting_Object.get_turner_cell()
            if ch == "SAVE":
                self.__Save_Load_Object.save_game(self.__Game_Setting_Object)
                sa = "Game Saved and EXIT"
                print(f'\n{sa:-^{2*len(sa)}}\n')
                exit()
            self.Game_Setting_Object.update_turn()

    def finish_game(self):
        winner = self.Game_Setting_Object.Board.check_winner()
        if winner:
            if self.Game_Setting_Object.Game_mode == 'multi':
                result = f'{winner} wins :|'
            else:
                if winner == self.Game_Setting_Object.Single_User_Mark:
                    result = 'User wins :)'
                else:
                    result = 'CPU wins :('
        else:
            result = 'No winner!'
        self.show_result(result)

    def show_result(self , result):
            os.system('cls')
            print('Game Result\n--------------')
            self.Game_Setting_Object.Board.display()
            print(result)


    def RUN(self):
        f = 1
        while f == 1:
            self.setup_game()
            self.run_game()
            self.finish_game()
            n = input("\nDo you wish to play agin? :) (y/n) : ").lower()
            match n:
                case "y": f = 1
                case "n": f = 0
        else:
            goodbye = "Thanks For Playing"
            l = len(goodbye) * 2
            print(f"\n{goodbye:-^{l}}\n")


class Load_Save():
    __slots__ = ["__loaded_setting_object"]

    def save_game(self , setting_object : GameSetting):
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path , "save.txt")
        packed_state = setting_object.pack_settings()
        with open(path , "w+" ) as file:
            file.write(str(packed_state))
    
    def load_game(self):
        print("\nGame is Loading ...")
        time.sleep(1)
        os.system("cls")
        try:
            path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(path, 'save.txt'), 'r') as file:
                dic = file.read()
                dic = eval(dic)

            board_list = dic['self.__Board']
            dic['self.__Board'] = Board(dic['self.__Board_dim'])
            dic['self.__Board'].BOARD = board_list

            match dic['self.__Game_mode']:
                case 'single':
                    dic['self.__Players'] = [HumanPlayer(dic['self.__Players'][0]) , CPUPlayer(dic['self.__Players'][1] , dic['self.__CPU_Level'][1])]
                case 'multi':
                    dic['self.__Players'] = [HumanPlayer(dic['self.__Players'][0]) , HumanPlayer(dic['self.__Players'][1])]
            self.__loaded_setting_object = GameSetting(dic)
            return self.__loaded_setting_object
        except:
            print('No file found!')
            exit()

        








        













        