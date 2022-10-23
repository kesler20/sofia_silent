import os

print("")
print("file:  ", __file__)
print("cwd:  ", os.getcwd())
print("base of file:  ", os.path.basename(__file__))
print("base of cwd:  ", os.path.basename(os.getcwd()))
print("dir of file:  ", os.path.dirname(__file__))

# to iterate through different folders
print("base of cwd:  ", os.path.dirname(
    __file__).split(r"\ ".replace(" ", "")))
