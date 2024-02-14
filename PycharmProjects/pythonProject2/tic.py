# game_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# current_player = 'X'
# input_count = 0
#
#
# def print_game_board():
#     for row in game_board:
#         print("|", end="")
#         for cell in row:
#             print(f" {cell} ", end="|")
#         print("\n-------------")
#     print()
#
#
# def check_horizontal():
#     for row in game_board:
#         if row[0] == row[1] == row[2]:
#             return True
#     return False
#
#
# def check_vertical():
#     for col in range(3):
#         if game_board[0][col] == game_board[1][col] == game_board[2][col]:
#             return True
#     return False
#
#
# def check_diagonal():
#
#     if game_board[0][0] == game_board[1][1] == game_board[2][2] or game_board[0][2] == game_board[1][1] == game_board[2][0]:
#         return True
#     return False
#
#
# def check_game_board():
#     if check_horizontal() or check_vertical() or check_diagonal():
#         return True
#     elif input_count == 9:
#         return False
#     else:
#         return None
#
#
# def place_character_on_board(position):
#     if position < 1 or position > 9:
#         print("Invalid position. Please enter a valid position (1-9).")
#         return 0
#
#     row = (position - 1) // 3
#     col = (position - 1) % 3
#
#     if isinstance(game_board[row][col], str):
#         print("Invalid position. Please enter a valid position (1-9).")
#         return 0
#
#     game_board[row][col] = current_player
#     return 1
#
#
# def run_game():
#     global current_player, input_count
#
#     while True:
#         print_game_board()
#         position = int(input(f"Player {current_player}, enter a position (1-9): "))
#
#         if place_character_on_board(position):
#             input_count += 1
#
#             if check_game_board() is True:
#                 print_game_board()
#                 print(f"Player {current_player} wins!")
#                 break
#             elif check_game_board() is False:
#                 print_game_board()
#                 print("It's a draw!")
#                 break
#
#             current_player = 'O' if current_player == 'X' else 'X'
#
#
# run_game()


# Function to get the enrollment semester based on the 3rd digit of the ID
def get_enrollment_semester(id):
    semester_mapping = {
        '1': 'Spring',
        '2': 'Fall',
        '3': 'Summer'
    }
    return semester_mapping.get(id[2], 'Unknown')

N = int(input())

e_data = {}

for i in range(N):
    student_id = input()
    l_three = student_id[-3:]
    semester = get_enrollment_semester(student_id)

    if semester in e_data:
        e_data[semester].append(l_three)
    else:
        e_data[semester] = [l_three]
print(e_data)

