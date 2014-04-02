import sys

# Checks if sys.argv array have not only file, but url as well
if len(sys.argv) < 2:
    print("Please enter directory path")
    quit()
else:
    path = sys.argv[1]
