import os
import sys


def get_symbols(files, symbols):
    """ Reads file and put symbols to array """
    while True:
        symbol = files.read(1).lower()
        if (symbol != ' ' and symbol != '' and symbol != '\n'):
            symbols.append(symbol)
        if not symbol:
            break
    print symbols
    return symbols


def get_words(f, words):
    """ Reads file and put words to array """
    text = ""
    word = ""
    while True:
        line = f.readline().lower()
        if not line:
            break
        text += line
    for i in text:
        if i.isalpha():
            word += i
        elif (len(word) > 0):
            words.append(word)
            word = ""
    print words
    return words


# Checks if sys.argv array have not only file, but url as well
if len(sys.argv) < 2:
    print("Please enter directory path")
    quit()
else:
    path = sys.argv[1]

files_array = []
# Creates array of all files in selected directory
for item_name in os.listdir(path):
    item_name = os.path.join(path, item_name)
    if (os.path.isfile(item_name) and item_name != path + '\statistics.txt'):
        files_array.append(item_name)

index = 0
# files array loop
for i in files_array:
    # Read symbols from file
    file = open(files_array[index], 'r')
    symbols = []
    get_symbols(file, symbols)
    file.close()
    # Read words from file
    file = open(files_array[index], 'r')
    words = []
    get_words(file, words)
    file.close()
    index += 1

print files_array
