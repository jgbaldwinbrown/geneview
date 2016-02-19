import sys

with open(sys.argv[1]) as f:
    for line in f:
        
        if line.isspace() or line[0] == '#':
            print line.strip() 
        else:
            name, rgb = line.strip().split('=')
            name = name.strip()
            rgb =  '#%02x%02x%02x' % tuple(map(int, rgb.strip().split(',')))
            print "'%s': '%s'" % (name, rgb.upper())

