import codecs
import csv

def open_file_list(filename, delimeter=',', cr='\n'):
    ''' Open a file, split it by line and return a list'''
    
    f = codecs.open(filename, encoding='utf-8', mode='r')
    output = []
    for row in f.read().split(cr)[:-1]:
        output.append(row.split(delimeter))
        
    return output

def open_file_dict(filename, key_column=None):
    f = codecs.open(filename, encoding='utf-8', mode='r')
    i = 0
    output = {}
    for row in f.read().split('\n')[:-1]:
        row = row.split('\t')
        if key_column is None:
            output[i] = row
            i += 1
        else:
            output[row[key_column]] = row
        
    return output

