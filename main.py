#!/bin/python3
# from pyndb import PYNDatabase
from pyntree import Node
import os

loc = os.getenv('HOME') + '/.config/'
db = Node(loc + 'hymbk.pyndb', autosave=True)


# First-time setup
if not db.has('bb'):
    db.bb = {}
    db.special = {}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def error(message):
    clear()
    print('=== ERROR! ===')
    print(message)
    input('Press enter to continue...')


def menu(title, *options, clearscreen=True):
    while True:
        if clearscreen: clear()
        x = menu_sub(title, *options)
        if x is not None: break
        error('Please choose one of the provided options.')
    return x


def menu_sub(title, *options):
    print('=' * 3, title, '=' * 3)
    print('[0] Back/Exit')
    for option, n in zip(options, range(1, len(options) + 1)):
        print(f'[{str(n)}] {option}')
    try:
        response = input('\n[>] ')
        # noinspection PyUnboundLocalVariable
        if response == '0':
            return False
        else:
            response = int(response) - 1
            return response if response < len(options) else None
    except ValueError:
        return None


def parse_reqs(songs):
    printed = {}
    for song in songs:
        song = song.lower().replace('\n', '')
        if song == '':
            pass
        elif song.isdigit():
            if db.bb.has(song):
                printed[song] = True
            else:
                printed[song] = False
                db.bb.set(song, {})
        else:
            if db.special.has(song):
                printed[song] = True
            else:
                printed[song] = False
                db.special.set(song, {})
    return printed


def weekly():
    clear()
    print('Type the numbers/names of the songs, or 0 to stop.')
    songs = []
    while True:
        r = input('[>] ')
        if r != '0':
            songs.append(r)
        else:
            break
    m = menu('Look good?', "Yes", "No", clearscreen=False)
    if m is False:
        return
    elif m == 0:
        printed = parse_reqs(songs)
        clear()
        for song in printed:
            print(f'{song} {"-" * (25 - len(song))} ({"📥" if printed[song] else "❌"})')
        input('Press enter to go back...')
    else:
        weekly()


def single(add):
    clear()
    print('Which songs would you like to add?' if add else 'Which songs would you like to remove?')
    print('(type 0 to go back)')
    while True:
        r = input('[>] ')
        if r == '0':
            break
        elif add:
            if db.bb.has(r) or db.special.has(r):
                print('That song has already been added!')
            else:
                if r.isdigit():
                    db.bb.set(r, {})
                else:
                    db.special.set(r, {})
        else:
            if not db.bb.has(r) and not db.special.has(r):
                print('Song not found!')
            else:
                if r.isdigit():
                    db.bb.delete(r)
                else:
                    db.special.delete(r)


def importer():
    while True:
        clear()
        print('Type the filename, or 0 to go back')
        r = input('[>] ')
        if r == '0':
            return
        try:
            f = open(r, 'r', encoding='utf-8-sig').readlines()
            break
        except OSError:
            error('File not found!')
    parse_reqs(f)
    input('Done! Press enter to continue...')


def view():
    print('From the hymnbook:')
    for song in db.bb._values:
        print(song)
    print('Others:')
    for song in db.special._values:
        print(song)
    input('Press enter to continue...')


def reset():
    for i in range(1, 4):
        if input(f'[{str(i)}/3] Are you sure (y/n) [>] ') != 'y':
            return
    db.delete('bb')          # Below is a workaround for pyndb bug #2
    db.delete('special')
    db.create('bb')
    db.create('special')
    print('Done! Press enter to continue...')


def main():
    while True:
        launch_to = menu('hymbk', "Add this week's songs",
                         "Add songs",
                         "Remove songs",
                         "Import previous songs from file",
                         "View printed hymns",
                         "Reset")
        if launch_to is False:
            exit()
        elif launch_to == 0:
            weekly()
        elif launch_to in (1, 2):
            single(1 if launch_to == 1 else 0)
        elif launch_to == 3:
            importer()
        elif launch_to == 4:
            view()
        elif launch_to == 5:
            reset()


if __name__ == '__main__':
    main()
