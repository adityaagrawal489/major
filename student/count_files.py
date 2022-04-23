import os

def count_files(loc):
    list = os.listdir(loc) # dir is your directory path
    number_files = len(list)
    return number_files