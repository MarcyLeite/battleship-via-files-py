import sys

BOARD_X = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
BOARD_Y = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
INVALID_LETTERS = ['K']
DIRECTION_HORIZONTAL = 'H'
DIRECTION_VERTICAL = 'V'

HIT_SCORE = 3
SUNK_BONUS = 2

TORPEDO_TOTAL = 25
SHIP_RULES = {
    # code: size, board_total
    1: [4, 5],
    2: [5, 2],
    3: [1, 10],
    4: [2, 5]
}

def read_file(file_name):
    file = open(f'./{file_name}.txt', 'r')
    data = file.read()
    file.close()
    return data.splitlines()

def get_position(pos_dir):
    x_number = pos_dir[1:]
    y_letter = pos_dir[0]

    if y_letter in INVALID_LETTERS:
        raise Exception('ERROR_POSITION_NONEXISTENT_VALIDATION')

    x = BOARD_X.index(x_number)
    y = BOARD_Y.index(y_letter)

    if x >= len(BOARD_X) or y >= len(BOARD_Y):
        raise Exception('ERROR_POSITION_NONEXISTENT_VALIDATION')

    return [x, y]

def create_ship(code, pos_dir):
    direction = DIRECTION_HORIZONTAL

    if SHIP_RULES[code][0] > 1:
        direction = pos_dir[-1]
        pos_dir = pos_dir[:-1]

    ship = []
    [x, y] = get_position(pos_dir)
    for _ in range(SHIP_RULES[code][0]):
        ship.append([x, y, False])
        if direction == DIRECTION_HORIZONTAL: x += 1
        elif direction == DIRECTION_VERTICAL: y += 1
    
    return ship

def add_ship_line_to_board(board, code, value_string):
    code = int(code)
    ship_list = value_string.split('|')
    if len(ship_list) != SHIP_RULES[code][1]:
        raise Exception('ERROR_NR_PARTS_VALIDATION')
    for pos_dir in ship_list:
        ship = create_ship(code, pos_dir)
        board.append(ship)

def add_torpedo_line_to_list(list, value_string):
    torpedo_list = value_string.split('|')
    if len(torpedo_list) != TORPEDO_TOTAL:
        raise Exception('ERROR_NR_PARTS_VALIDATION')
    for torpedo in torpedo_list:
        pos = get_position(torpedo)
        list.append(pos)

def check_ship_overlap(board):
    piece_list = []
    for ship in board:
        for coords in ship:
            if coords in piece_list: raise Exception('ERROR_OVERWRITE_PIECES_VALIDATION')
            piece_list.append(coords)

def read_player(file_name):
    data = read_file(file_name)

    board = []
    torpedo_list = []
    for line in data:
        if line == '#Jogada':
            continue

        [code, value_string] = line.split(';')
        if code == 'T':
            add_torpedo_line_to_list(torpedo_list, value_string)
            continue    
        
        add_ship_line_to_board(board, code, value_string)
        check_ship_overlap(board)

    return [board, torpedo_list]

def hit_ship(ship, torpedo):
    for pos_hit in ship:
        if torpedo[0] == pos_hit[0] and torpedo[1] == pos_hit[1]:
            pos_hit[2] = True

def resolve_board(board, torpedo_list):
    for torpedo in torpedo_list:
        for ship in board:
            hit_ship(ship, torpedo)

def get_ship_result(ship):
    points = 0
    hit_count = 0
    for pos_hit in ship:
        if pos_hit[2]:
            hit_count += 1
            points += 3
    if hit_count == len(ship):
        points += 2
    
    return points

def get_score(board):
    points = 0
    hit = 0
    miss = 0
    for ship in board:
        ship_point = get_ship_result(ship)
        if ship_point == 0: miss += 1
        else: hit += 1
        points += ship_point

    return [points, hit, miss]
        
def write_string_in_result(write_str):
    file = open('resultado.txt', 'w')
    file.write(write_str)
    file.close()

def generate_result_string(player, score):
    write_str = f'J{player} {score[1]}AA {score[2]}AE {score[0]}PT'
    return write_str

def write_error(message):
    write_string_in_result(message)


if __name__ == '__main__':
    err_scope = ''
    try:
        err_scope = 'J1'
        [board_1, torpedo_list_1] = read_player('jogador1')
        err_scope = 'J2'
        [board_2, torpedo_list_2] = read_player('jogador2')
        resolve_board(board_1, torpedo_list_2)
        resolve_board(board_2, torpedo_list_1)

        score_1 = get_score(board_2)
        score_2 = get_score(board_1)

        if score_1[0] > score_2[0]:
            result_string = generate_result_string(1, score_1)
            write_string_in_result(result_string)
        if score_1[0] < score_2[0]:
            result_string = generate_result_string(2, score_2)
            write_string_in_result(result_string)
        if score_1[0] == score_2[0]:
            result_string = generate_result_string(1, score_1)
            result_string += f'\n{generate_result_string(2, score_2)}'
            write_string_in_result(result_string)
    except Exception as err:
        write_error(f'{err_scope} {str(err)}')

