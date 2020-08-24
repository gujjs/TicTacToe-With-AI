from random import randint
from collections import deque
import copy


board = {3: {1: ' ', 2: ' ', 3: ' '},
         2: {1: ' ', 2: ' ', 3: ' '},
         1: {1: ' ', 2: ' ', 3: ' '},
         'T': {'T': 'X', 'nx': 0, 'no': 0,
               'available': ['3 1', '3 2', '3 3', '2 1', '2 2', '2 3', '1 1', '1 2', '1 3'],
               'removed': []}
         }


def print_board():
    print("---------")
    print("|", board[3][1], board[3][2], board[3][3], "|")
    print("|", board[2][1], board[2][2], board[2][3], "|")
    print("|", board[1][1], board[1][2], board[1][3], "|")
    print("---------")


def startup():
    seq = input("Enter cells:")
    i = 0
    for key in board:
        if key != 'T':
            for slot in board[key]:
                if seq[i] == '_':
                    board[key][slot] = ' '
                else:
                    board[key][slot] = seq[i]
                i += 1
    print_board()


def enter(symbol):
    inp = input("Enter the coordinates:").strip().split(' ')

    if len(inp) != 2:
        print("You should enter numbers!")
        enter(symbol)
        return

    try:
        inp = [int(i) for i in inp]
    except ValueError:
        print("You should enter numbers!")
        enter(symbol)
        return
    else:
        for i in inp:
            if i < 1 or i > 3:
                print("Coordinates should be from 1 to 3!")
                enter(symbol)
                return

    x = inp[1]
    y = inp[0]

    if board[x][y] != ' ':
        print("This cell is occupied! Choose another one!")
        enter(symbol)
    else:
        board['T']['available'].remove(str(x) + ' ' + str(y))
        board['T']['removed'].append(str(x) + ' ' + str(y))
        board[x][y] = symbol


def check_win(*input_board):
    check_diagonal = []
    diagonal_reverse = []
    draw = True
    check_board = board

    if input_board:
        check_board = array_to_board(input_board[0])

    for key in check_board:
        if key != 'T':
            check_list = list(check_board[key].values())
            if all_same_list(check_list):
                return check_list[0] + " wins"

            if ' ' in check_list:
                draw = False

            check_list = []
            for element in check_board:
                if element != 'T':
                    check_list.append(check_board[element][key])
            if all_same_list(check_list):
                return check_list[0] + " wins"

            check_diagonal.append(check_board[key][key])
            diagonal_reverse.append(check_board[key][4 - key])

    if all_same_list(check_diagonal):
        return check_diagonal[0] + " wins"

    if all_same_list(diagonal_reverse):
        return diagonal_reverse[0] + " wins"

    if draw:
        return "Draw"
    else:
        return False


def all_same_list(lis):
    return all([elem == lis[0] for elem in lis]) and (lis[0] == 'X' or lis[0] == 'O')


def two_same_list(lis):
    if ' ' in lis:
        ind = lis.index(' ')
        lis.pop(ind)
        if lis[0] == lis[1]:
            return ind
    else:
        return False


def random_move(mode, symbol):
    choice_ind = randint(0, len(board["T"]['available']) - 1)
    choice = board["T"]['available'].pop(choice_ind)
    board["T"]['removed'].append(choice)
    choice = choice.split(' ')
    board[int(choice[0])][int(choice[1])] = symbol
    print('Making move level "{}"'.format(mode))
    print_board()


def essential_move(mode, symbol):
    buffer = deque()
    check_diagonal = []
    diagonal_reverse = []
    win = False

    for key in board:
        if key != 'T':
            check_list = list(board[key].values())
            check = two_same_list(check_list)
            if check and check_list[check - 1] == symbol:
                buffer.appendleft(str(key) + ' ' + str(check + 1))
                win = True
                break
            elif check and check_list[check - 1] != ' ':
                buffer.append(str(key) + ' ' + str(check + 1))

    for key in board:
        if key != 'T' and not win:
            check_list = []
            for element in board:
                if element != 'T':
                    check_list.append(board[element][key])
            check = two_same_list(check_list)

            if check and check_list[check - 1] == symbol:
                buffer.appendleft(str(3 - check) + ' ' + str(key))
                win = True
                break
            elif check and check_list[check - 1] != ' ':
                buffer.append(str(3 - check) + ' ' + str(key))

            check_diagonal.append(board[key][key])
            diagonal_reverse.append(board[key][4 - key])

    if not win:
        check = two_same_list(check_diagonal)
        if check and check_diagonal[check - 1] == symbol:
            choice = str(check + 1) + ' ' + str(check + 1)

            buffer.appendleft(choice)
            # board[check + 1][check + 1] = symbol
            win = True
        elif check and check_diagonal[check - 1] != ' ':
            buffer.append(str(check + 1) + ' ' + str(check + 1))

        check = two_same_list(diagonal_reverse)
        if check and diagonal_reverse[check - 1] == symbol:
            buffer.appendleft(str(3 - check) + ' ' + str(check + 1))
            # board[3 - check][check + 1] = symbol
            win = True
        elif check and diagonal_reverse[check - 1] != ' ':
            buffer.append(str(3 - check) + ' ' + str(check + 1))

    if buffer:
        # print(buffer, 'buffer')
        for position in buffer:
            if position in board['T']['available']:
                y = int(position.split(' ')[0])
                x = int(position.split(' ')[1])
                print('Making move level "{}"'.format(mode))
                board[y][x] = symbol
                board["T"]['available'].remove(position)
                board["T"]['removed'].append(position)
                print_board()
                return True

    return False


def board_to_array(value):
    array = []
    for key in value:
        if key != 'T':
            array.extend(value[key].values())

    for x in array:
        if x == ' ':
            array[array.index(x)] = array.index(x)

    return array


def array_to_board(arr):
    check_board = {3: {1: ' ', 2: ' ', 3: ' '},
                   2: {1: ' ', 2: ' ', 3: ' '},
                   1: {1: ' ', 2: ' ', 3: ' '},
                   }
    ind = 0

    for key in check_board:
        for sub_key in check_board[key]:
            if isinstance(arr[ind], str):
                check_board[key][sub_key] = arr[ind]
            else:
                check_board[key][sub_key] = ' '
            ind += 1
    return check_board


def hard_move(symbol, *args):
    move_count = 1
    working_board = board_to_array(board)

    if len(args) == 2:
        working_board = copy.deepcopy(args[0])
        move_count = args[1] + 1

    res = check_win(working_board)
    if res:
        if res[0] == 'D':
            return [0]
        elif res[0] == symbol:
            return [1]
        elif res[0] == opposite_move(symbol):
            return [-1]

    options = dict([(x, 0) for x in working_board if isinstance(x, int)])

    for x in options.keys():
        temporary_board = copy.deepcopy(working_board)

        if move_count % 2 == 1:
            temporary_board[x] = symbol
        elif move_count % 2 == 0:
            temporary_board[x] = opposite_move(symbol)

        options[x] += hard_move(symbol, temporary_board, move_count)[0]

    for index, value in options.items():
        if move_count % 2 == 1 and value == max(options.values()):
            return value, index
        elif move_count % 2 == 0 and value == min(options.values()):
            return value, index


def make_hard_move(position, symbol):
    y = 3 - position // 3
    x = position % 3 + 1
    board["T"]['available'].remove(str(y) + ' ' + str(x))
    board["T"]['removed'].append(str(y) + ' ' + str(x))
    board[y][x] = symbol


def opposite_move(symbol):
    if symbol == 'X':
        return 'O'
    elif symbol == 'O':
        return 'X'


def move_handler(mode, symbol):
    if mode == 'user':
        enter(symbol)
    elif mode == 'medium':
        if not essential_move(mode, symbol):
            random_move(mode, symbol)
    elif mode == 'easy':
        random_move(mode, symbol)
    elif mode == 'hard':
        pos = hard_move(symbol)[1]
        make_hard_move(pos, symbol)

    print_board()
    if check_win():
        print(check_win(), 'check win ')
        reset()
        return True


def reset():
    board["T"]['available'].extend(board["T"]['removed'])
    board["T"]['removed'] = []
    for key in board:
        if key != "T":
            for lower_key in board[key]:
                board[key][lower_key] = ' '


def starting_command():
    result = input("Input command:").split(" ")
    if len(result) == 3 and result[0] == 'start':
        result.pop(0)
        for x in result:
            if x != 'easy' and x != 'user' and x != 'medium' and x != 'hard':
                print('Bad parameters!')
                return starting_command()
        return result
    elif result[0] == 'exit':
        return False
    else:
        print('Bad parameters!')
        return starting_command()


def start():
    while True:
        parameters = starting_command()
        if not parameters:
            break
        else:
            print_board()
        while True:
            if move_handler(parameters[0], 'X'):
                break
            if move_handler(parameters[1], 'O'):
                break


start()
