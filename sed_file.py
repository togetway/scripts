#-*- coding:utf-8 -*-
import os,sys

def sed_file(filename, old_text, new_text):
    if not os.path.isfile(filename):
        print '%s is not exist.' % filename
        return False

    with open(filename,'r') as f:
        lines = f.readlines()

    if not lines:
        print '%s is Null' % filename
        return False

    ou = open(filename, 'w')
    for line in lines:
        new_line = line.replace(old_text, new_text)
        ou.write(new_line)
    ou.close()

def help():
    print "Usage: ./sed_file.py filename old_text new_text"


if __name__ == '__main__':
    if len(sys.argv) != 4:
        help()
    else:
        filename = sys.argv[1]
        old_text = sys.argv[2]
        new_text = sys.argv[3]
        sed_file(filename, old_text, new_text)

    

