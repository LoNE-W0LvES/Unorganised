from sys import argv

result = f"{argv[1]} is a palindrome." if (
        str(argv[1]).replace(" ", "").lower() ==
        str(argv[1]).replace(" ", "").lower()
        [::-1])else f"{argv[1]} is not a palindrome."

print('\n' + 'Output: ' + result + '\n')
