import os
import collections
import sys


def counter(array, dictionary):
    """ Puts array members (directory files) to dictionaries """
    for x in array:
        if x not in dictionary.keys():
            dictionary[x] = 1
        else:
            dictionary[x] += 1
    return dictionary


def get_symbols(files, symbols):
    """ Reads file and put symbols to array """
    while True:
        symbol = files.read(1).lower()
        if (symbol != ' ' and symbol != '' and symbol != '\n'):
            symbols.append(symbol)
        if not symbol:
            break
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
    return words


files_array = []

# Checks if sys.argv array have not only file, but url as well
if len(sys.argv) < 2:
    print("Enter directory path")
    quit()
# Checks if directory exists
elif not os.path.isdir(sys.argv[1]):
    print("Directory path is entered incorrectly")
    quit()
else:
    path = sys.argv[1]

# Creates array of all files in selected directory
for item_name in os.listdir(path):
    item_name = os.path.join(path, item_name)
    if (os.path.isfile(item_name) and item_name != path + '\statistics.txt'):
        files_array.append(item_name)

# Creates statistics file in directory we read files
f = open(path + '\statistics.txt', 'w+')
index = 0
all_words = []
all_symbols = []
num = 0
# All files in directory loop
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
    dict_symbols = {}
    dict_symbols_all = {}
    dict_words = {}
    dict_words_all = {}
    all_words.extend(words)
    all_symbols.extend(symbols)
    one_dict_symbols = counter(symbols, dict_symbols)
    all_dict_symbols = counter(all_symbols, dict_symbols_all)
    one_dict_words = counter(words, dict_words)
    all_dict_words = counter(all_words, dict_words_all)
    num += 1
    # Write symbols and words statistics of individual files
    f.write("%d file: " % num + files_array[index] + " \nSymbols: \n")
    for symbol, times in one_dict_symbols.items():
        f.write('Symbol: "' + symbol + '" repeats: ' + str(times) + 'x \n')
    f.write("Words:\n")
    for word, times in one_dict_words.items():
        f.write('Word: "' + word + '" repeats: ' + str(times) + 'x \n')
    index += 1

# Write symbols and words statistics of all files
f.write("\nAll files statistics: \nSymbols: \n")
for symbol, times in all_dict_symbols.items():
    f.write('Symbol: "' + symbol + '" repeats: ' + str(times) + 'x \n')
f.write("Words:\n")
for word, times in all_dict_words.items():
    f.write('Word: "' + word + '" repeats: ' + str(times) + 'x \n')
f.close()
