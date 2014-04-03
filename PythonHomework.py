import os
import sys

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

# Looking if all files were added to files array
print files_array
