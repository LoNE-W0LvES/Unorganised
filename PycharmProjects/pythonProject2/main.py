# s = input("String: ")
# out = ""
# lower = 0
# upper = 0
# # for c in s:
#
#     # if c.islower():
#     #     lower += 1
#     # else:
#     #     upper += 1
#
# for i in range(len(s)):
#
#     if s[i].islower():
#         lower += 1
#     else:
#         upper += 1
#
# out = s.upper() if upper > lower else s.lower()
#
# if upper > lower:
#     out = s.upper()
# elif lower > upper:
#     out = s.lower()
# print(out)
#
#

# s = input("Write: ")
# out = ""
# num = 0
# alpha = 0
# arrNum = []
# arrWord = []
# for c in s:
#     if c.isnumeric():
#         arrNum.append(int(c))
#         num += 1
#     if c.isalpha():
#         arrWord.append(c)
#         alpha += 1
# arrNum.sort()
# # arrNum.pop(3)
# # arrNum.pop(4)
# print(arrNum)
# print(arrWord)
# if alpha == 0 and num > 0:
#     print("NUMBER")
# if alpha > 0 and num > 0:
#     print("MIXED")
# if alpha > 0 and num == 0:
#     print("WORD")


# s0 = input("Input 1st String: ")
# s1 = input("Input 2nd String:: ")
# s = ''
# for i in s0:
#     for j in s1:
#         if i.:
#             s += i
#             break
#
# s += i
# for i in s1:
#     for j in s0:
#         if i == j:
#             s += i
#             break
#
# print(s)
# harry


# a = []
# while True:
#     s = input()
#     if s == "STOP":
#         break
#     a.append(int(s))
# res = []
#
# for x in a:
#     if x not in res:
#         res.append(x)
#         print(res)
#         print(str(x) + " - " + str(a.count(x)) + " times")


# s0 = input("Input New Password: ")
#
# s_char = "[@_!#$%^&*()<>?/|}{~:]"
#
# c_s_char = 0
# c_digit = 0
# c_upper = 0
# c_lower = 0
#
# for i in s0:
#     if i.isupper():
#         c_upper += 1
#     if i.islower():
#         c_lower += 1
#     if i.isnumeric():
#         c_digit += 1
#     if i in s_char:
#         c_s_char += 1
#
# if c_upper == 0:
#     print("Uppercase character missing")
# if c_lower == 0:
#     print("Lowercase character missing")
# if c_digit == 0:
#     print("Digit missing")
# if c_s_char == 0:
#     print("Special character missing")
#
# if c_upper > 0 and c_lower > 0 and c_digit > 0 and c_lower > 0:
#     print("OK")

# s0 = input("Input an list: ").split(" ")
# s0 = [int(i) for i in input("Input 1st list: ").split(" ")]
# s1 = [int(i) for i in input("Input 2nd list: ").split(" ")]
# result = []
#
# for num1 in s0:
#     for num2 in s1:
#         result.append(num1 * num2)
#
# print(result)

# s0 = [int(i) for i in input("Input 1st list: ").split(" ")]
# def is_ub_jumper(sequence):
#     n = len(sequence)
#     differences = set()
#
#     for i in range(1, n):
#         diff = abs(sequence[i] - sequence[i - 1])
#         if diff >= 1 and diff <= n - 1:
#             differences.add(diff)
#
#     return len(differences) == n - 1
#
#
# while True:
#     user_input = input("Enter a number sequence (or 'STOP' to exit): ")
#     if user_input == "STOP":
#         break
#
#     numbers = [int(num) for num in user_input.split()]
#     if is_ub_jumper(numbers):
#         print("The sequence is a UB Jumper")
#     else:
#         print("The sequence is not a UB Jumper")

# def is_ub_jumper(sequence):
#     n = len(sequence)
#     differences = set()
#
#     for i in range(1, n):
#         diff = abs(sequence[i] - sequence[i - 1])
#         if diff >= 1 and diff <= n - 1:
#             differences.add(diff)
#
#     return len(differences) == n - 1


# while True:
#     user_input = input("Enter a number list (or 'STOP' to exit): ")
#     if user_input == "STOP":
#         break
#
#     num = [int(num) for num in user_input.strip("\n").split(" ")]
#
#     n = len(num)
#     differences = set()
#
#     for i in range(1, n):
#         diff = abs(num[i] - num[i - 1])
#         if diff >= 1 and diff <= n - 1:
#             differences.add(diff)
#
#     if len(differences) == n - 1:
#         print("UB Jumper")
#     else:
#         print("Not UB Jumper")


# dict_str1 =
# dict_str2 = input()

# dict1 = {}
# dict2 = {}
# com_dict = {}
# for item in input().split(","):
#     dict1.update({item.split(":")[0]: int(item.split(":")[1])})
# for item in input().split(","):
#     dict2.update({item.split(":")[0]: int(item.split(":")[1])})
#
# for key in dict1:
#     if key in dict2:
#         com_dict[key] = dict1[key] + dict2[key]
#     else:
#         com_dict[key] = dict1[key]
#
# # Add remaining keys from dict2
# for key in dict2:
#     if key not in dict1:
#         com_dict[key] = dict2[key]
#
# values = set(com_dict.values())
# sorted_values = tuple(sorted(values))
#
# print(com_dict)
# print(sorted_values)


# numbers = []
# frequency = {}
#
# while True:
#     num = input()
#     if num.upper() == "STOP":
#         break
#     else:
#         numbers.append(int(num))
#
# for number in numbers:
#     if number in frequency:
#         frequency[number] += 1
#     else:
#         frequency[number] = 1
#
# for number, count in frequency.items():
#     print(f"{number} - {count} times")

# dictionary = {}
# for item in input().replace(" ", "").split(","):
#     dictionary.update({item.split(":")[0]: item.split(":")[1]})
#
# inv_dict = {}
#
# for key, value in dictionary.items():
#     if value in inv_dict:
#         inv_dict[value].append(key)
#     else:
#         inv_dict[value] = [key]
#
# print(inv_dict)


# key_mapping = {
#     '.': '1',
#     ',': '11',
#     '?': '111',
#     '!': '1111',
#     ':': '11111',
#     'A': '2', 'B': '22', 'C': '222',
#     'D': '3', 'E': '33', 'F': '333',
#     'G': '4', 'H': '44', 'I': '444',
#     'J': '5', 'K': '55', 'L': '555',
#     'M': '6', 'N': '66', 'O': '666',
#     'P': '7', 'Q': '77', 'R': '777', 'S': '7777',
#     'T': '8', 'U': '88', 'V': '888',
#     'W': '9', 'X': '99', 'Y': '999', 'Z': '9999',
#     ' ': '0'
# }
# key_presses = []
#
# message = input("Enter your message: ").upper()
# for char in message:
#     if char in key_mapping:
#         key_presses.append(key_mapping[char])
#
# print(''.join(key_presses))


# n, k = map(int, input().split(" "))
# per = [int(x) for x in input().split(" ")]
# valids = 0
#
# for i in range(n):
#     if per[i] + k <= 5:
#         valids += 1
# print(valids // 3)


# inputBMI = [int(x) for x in input().replace('(', '').replace(')', '').replace(' ', '').split(',')]
# height = inputBMI[0]
# weight = inputBMI[1]
# height_m = height / 100
# bmi = weight / (height_m ** 2)
# if bmi < 18.5:
#     condition = "Underweight"
# elif 18.5 <= bmi <= 24.9:
#     condition = "Normal"
# elif 25 <= bmi <= 30:
#     condition = "Overweight"
# else:
#     condition = "Obese"
# print(f"Score is {round(bmi, 1)}. You are {condition}")


# def BMI(height, weight):
#     height_m = height / 100
#
#     bmi = weight / (height_m ** 2)
#
#     if bmi < 18.5:
#         condition = "Underweight"
#     elif 18.5 <= bmi <= 24.9:
#         condition = "Normal"
#     elif 25 <= bmi <= 30:
#         condition = "Overweight"
#     else:
#         condition = "Obese"
#     print(f"Score is {round(bmi, 1)}. You are {condition}")
#
#
# inputBMI = [int(x) for x in input().replace('(', '').replace(')', '').replace(' ', '').split(',')]
# BMI(inputBMI[0], inputBMI[1])



# inputFood = [x.lower() for x in input().replace('(', '').replace(')', '').replace(' ', '').replace("'", '').split(',')]
# place = "mohakhali" if len(inputFood) == 1 else inputFood[1]
# menuP = {"bbqchickencheeseburger": 250, "beefburger": 170, "nagadrums": 200}
#
# if inputFood[0] in menuP:
#     print(menuP[inputFood[0]] + (40 if place == "mohakhali" else 60) + (menuP[inputFood[0]] * 0.08))
#

# inputFood = [x.lower() for x in input().replace('(', '').replace(')', '').replace(' ', '').replace("'", '').split(',')]
# def order(food, location = "mohakhali"):
#     menuP = {"bbqchickencheeseburger": 250, "beefburger": 170, "nagadrums": 200}
#     if food in menuP:
#         print(menuP[food] + (40 if location == "mohakhali" else 60) + (menuP[food] * 0.08))
#
# inputFood = [x.lower() for x in input().replace('(', '').replace(')', '').replace(' ', '').replace("'", '').split(',')]
# place = "mohakhali" if len(inputFood) == 1 else inputFood[1]
# order(inputFood.replace(' ', '').lower())
#
#

# def order(food, location="mohakhali"):
#     menu_p = {
#         "bbqchickencheeseburger": 250,
#         "beefburger": 170,
#         "nagadrums": 200
#     }
#
#     if food in menu_p:
#         print(menu_p[food] + (40 if location == "mohakhali" else 60) + (menu_p[food] * 0.08))
#
#
# inputFood = [x.lower() for x in input().replace('(', '').replace(')', '').replace(' ', '').replace("'", '').split(',')]
# if len(inputFood) > 0:
#     order(inputFood[0], inputFood[1])
# else:
#     order(inputFood[0])
# ('Beef Burger', 'mohakhali')
# def replace_domain(email, new_domain, old_domain="kaaj.com"):
#     if old_domain in email:
#         username, domain = email.split("@")
#         print(username, domain)
#         if domain == old_domain:
#             print("Changed: ", username + "@" + new_domain)
#         else:
#             print("Unchanged: ", email)
#
#
# eAD = input().strip("(").strip(")").replace("'", '').replace(" ", '').split(",")
#
# print(eAD)
#
# if len(eAD) == 1:
#     replace_domain(eAD[0], eAD[1])
# else:
#     replace_domain(eAD[0], eAD[1], eAD[2])

from math import floor
# eAD = input().replace(' ', '')
# print("Palindrome" if 1 in [1 for i in range(int(len(eAD)/2)) if eAD[i] == eAD[len(eAD) - i - 1]] else "Not a palindrome")

# eAD = int(input())

# y = dInput//365
# m = (dInput - (dInput//365) * 365) // 30
# d = (dInput - (dInput//365) * 365 - ((dInput - (dInput//365) * 365) // 30) * 30)


# def ymd(dinput):
#     print(f"{dinput//365}years, {(dinput - (dinput//365) * 365) // 30} months and {(dinput - (dinput//365) * 365 - ((dinput - (dinput//365) * 365) // 30) * 30)} days")
#
# ymd(int(input()))


# def cap_paragraph(paragraph):
#     p1 = paragraph.capitalize()
#     for j in [". ", "! ", "? "]:
#         p0 = p1.split(j)
#         p1 = p0[0]
#         if len(p0) > 0:
#             for i in range(1, len(p0)):
#                 p1 = p1 + j + p0[i].capitalize()
#     return p1.replace(" i ", "I ")
#
# print(cap_paragraph(input().replace('(', '').replace(')', '').replace("'", '')))



game_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
current_player = 'X'
input_count = 0


def print_game_board():
    for row in game_board:
        print("|", end="")
        for cell in row:
            print(f" {cell} ", end="|")
        print("\n-------------")
    print()


def check_horizontal():
    for row in game_board:
        if row[0] == row[1] == row[2]:
            return True
    return False


def check_vertical():
    for col in range(3):
        if game_board[0][col] == game_board[1][col] == game_board[2][col]:
            return True
    return False


def check_diagonal():

    if game_board[0][0] == game_board[1][1] == game_board[2][2] or game_board[0][2] == game_board[1][1] == game_board[2][0]:
        return True
    return False


def check_game_board():
    if check_horizontal() or check_vertical() or check_diagonal():
        return True
    elif input_count == 9:
        return False
    else:
        return None


def place_character_on_board(position):
    if position < 1 or position > 9:
        print("Invalid position. Please enter a valid position (1-9).")
        return 0

    row = (position - 1) // 3
    col = (position - 1) % 3

    if isinstance(game_board[row][col], str):
        print("Invalid position. Please enter a valid position (1-9).")
        return 0

    game_board[row][col] = current_player
    return 1


def run_game():
    global current_player, input_count

    while True:
        print_game_board()
        position = int(input(f"Player {current_player}, enter a position (1-9): "))

        if place_character_on_board(position):
            input_count += 1

            if check_game_board() is True:
                print_game_board()
                print(f"Player {current_player} wins!")
                break
            elif check_game_board() is False:
                print_game_board()
                print("It's a draw!")
                break

            current_player = 'O' if current_player == 'X' else 'X'


run_game()