import sys

def flast(pieces):
    username = pieces[0][0] + pieces[-1]
    return username.lower()


def firstdotlast(pieces):
    username = pieces[0] + '.' + pieces[-1]
    return username.lower()


def firstlast(pieces):
    username = pieces[0] + pieces[-1]
    return username.lower()


def firstl(pieces):
    username = pieces[0] + pieces[-1][0]
    return username.lower()


def first(pieces):
    username = pieces[0]
    return username.lower()


def filast(pieces):
    username = pieces[0][:2] + pieces[-1]
    return username.lower()


def fila(pieces):
    username = pieces[0][:2] + pieces[-1][:2]
    return username.lower()


def alldot(pieces):
    username = '.'.join(pieces)
    return username.lower()


def fmlast(pieces):
    username = pieces[0][0] + pieces[1][0] + pieces[2]
    return username.lower()



args = sys.argv[1]
users = args.split(',')
for user in users:
    pieces = user.split()
    print(flast(pieces))
    print(firstdotlast(pieces))
    print(firstlast(pieces))
    print(firstl(pieces))
    print(first(pieces))
    print(filast(pieces))
    if (len(pieces) > 2):
        print(alldot(pieces))
    if (len(pieces) == 3):
        print(fmlast(pieces))