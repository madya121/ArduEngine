import json
import os
import sys
from distutils.dir_util import copy_tree
from shutil import copy

import re

PLACEHOLDER = re.compile('\\$([^\\$]+)\\$')

class Snippet:
	last = None
	def __init__(self, owner, text, postfix):
		self.owner = owner
		if self.owner.last is not None:
			with self.owner.last:
				pass
		self.owner.write("".join(text))
		self.owner.last = self
		self.postfix = postfix

	def __enter__(self):
		self.owner.write("{")
		self.owner.current_indent += 1
		self.owner.last = None

	def __exit__(self, a, b, c):
		if self.owner.last is not None:
			with self.owner.last:
				pass
		self.owner.current_indent -= 1
		self.owner.write("}" + self.postfix)

class Subs:
	def __init__(self, owner, subs):
		self.owner = owner
		self.subs = subs

	def __enter__(self):
		self.owner.substack = [self.subs] + self.owner.substack

	def __exit__(self, a, b, c):
		self.owner.substack = self.owner.substack[1:]


class CodeFile:
	def __init__(self, filename):
		self.current_indent = 0
		self.last = None
		self.out = open(filename,"w")
		self.indent = "\t"
		self.substack = []

	def close(self):
		self.out.close()
		self.out = None

	def write(self, x, indent=0):
		self.out.write(self.indent * (self.current_indent+indent) + x + "\n")

	def format(self, text):
		while True:
			m = PLACEHOLDER.search(text)
			if m is None:
				return text
			s = None
			for sub in self.substack:
				if m.group(1) in sub:
					s = sub[m.group(1)]
					break
			if s is None:
				raise Exception("Substitution '%s' not set." % m.groups(1))
			text = text[:m.start()] + str(s) + text[m.end():]

	def subs(self, **subs):
		return Subs(self, subs)

	def __call__(self, text):
		self.write(self.format(text))

	def block(self, text, postfix=""):
		return Snippet(self, self.format(text), postfix)

class CppFile(CodeFile):
	def __init__(self, filename):
		CodeFile.__init__(self, filename)

	def label(self, text):
		self.write(self.format(text) + ":", -1)

__all__ = [ "CppFile", "CodeFile" ]

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
        
def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear')

getch = _Getch()











def display_scenes_table():
    files = os.listdir('Scenes/')
    
    indx = 1
    for i in range(50):
        print ('#', end='')
    print ()
    print ('#\tList Of Scenes'.ljust(43) + '#')
    for i in range(50):
        print ('#', end='')
    print ()
    
        
    for file in files:
        if file.endswith('.cpp'):
            print (('#\t' + (str(indx) + ". ").ljust(3) + file[:-4]).ljust(43) + '#')
            indx = indx + 1
        
    for i in range(50):
        print ('#', end='')
    print ()
    
def generate_game_scene(scene_name):
    cpp = CppFile('Scenes/' + scene_name + '.cpp')
    cpp('#ifndef ' + scene_name + '_CPP')
    cpp('#define ' + scene_name + '_CPP')

    cpp('\n#include "../ArduEngine/ArduEngine.h"\n')

    cpp('#include "../Images.h"')
    cpp('#include "../SceneManager.cpp"\n')

    with cpp.subs(name=scene_name):
        with cpp.block('class $name$ : public ArduScene', ';'):
            cpp.label('public')
            with cpp.block(scene_name + '(ArduEngine &engine, uint8_t sceneID) : ArduScene(sceneID, engine)'):
                cpp('// This will be called once when the game start')
                cpp('logo = new ArduSprite(0, 0, 128, 64, WHITE, arduengine_splash, engine);')
            with cpp.block('void Load(ArduEngine &engine)'):
                cpp('// This will be called once everytime we enter this scene')
            with cpp.block('void Run(ArduEngine &engine)'):
                cpp("// This will be called every frame when we're in this scene")
            with cpp.block('void Destroy(ArduEngine &engine)'):
                cpp('// This will be called once everytime we leave this scene')

            cpp.label('\nprivate')
            cpp('  ArduSprite *logo;')
    cpp('')

    cpp('\n#endif')
    cpp.close()
    
def generate_scene_id(name):
    result = '';
    for c in name:
        if c.isupper():
            result = result + '_'
        result = result + c.upper()
    
    return result[1:] + '_SCENE_ID'
    
def generate_scene_variable(name):
    return name[:1].lower() + name[1:-4]
    
def generate_scene_manager():
    files = os.listdir('Scenes/')

    cpp = CppFile('SceneManager.cpp')
    cpp('#ifndef SCENE_MANAGER_CPP')
    cpp('#define SCENE_MANAGER_CPP')
    
    cpp('')
    
    for file in files:
        if file.endswith('.cpp'):
            cpp('#include "Scenes/' + file + '"')
    
    cpp('')
    
    for i in range(len(files)):
        if (files[i].endswith('.cpp')):
            id = generate_scene_id(files[i][:-4])
            cpp('const uint8_t ' + id + ' = ' + str(i) + ';')
    
    cpp('')
    
    with cpp.block('class SceneManager', ';'):
        cpp.label('public')
        
        for file in files:
            if file.endswith('.cpp'):
                var = generate_scene_variable(file)
                cpp(file[:-4] + ' *' + var + ';')
            
        cpp('')
        
        with cpp.block('SceneManager(ArduEngine &engine)'):
            
            for file in files:
                if file.endswith('.cpp'):
                    var = generate_scene_variable(file)
                    id  = generate_scene_id(file[:-4])
                    cpp(var + ' = new ' + file[:-4] + '(engine, ' + id + ');')
    
    cpp('#endif')
    cpp.close()

MAIN_MENU = 1
CREATE_SCENE = 2
DELETE_SCENE = 3

ACTIVE_MENU = MAIN_MENU

def main_menu():
    global ACTIVE_MENU
    global MAIN_MENU
    global CREATE_SCENE
    global DELETE_SCENE

    print ()
    print ()
    print ('1. Create New Scene')
    print ('2. Delete Scene')
    print ('3. Refresh Scene Manager')
    print ()
    
    try:
        input = getch().decode('utf-8')
        
        if input == '1':
            ACTIVE_MENU = CREATE_SCENE
        elif input == '2':
            ACTIVE_MENU = DELETE_SCENE
        elif input == '3':
            os.remove('SceneManager.cpp')
            generate_scene_manager()
            
    except:
        input = ''
    
    if input == 'q':
        clear()
        sys.exit()
        
def create_scene():
    global ACTIVE_MENU
    global MAIN_MENU
    global CREATE_SCENE
    global DELETE_SCENE

    print ()
    print ()
    print ('Scene name (No Space, AlphaNumeric Only. \'!cancel\' to cancel): ', end='')
    scene = input()
    
    ACTIVE_MENU = MAIN_MENU
    
    if (scene == '!cancel'):
        return
    
    generate_game_scene(scene)
    os.remove('SceneManager.cpp')
    generate_scene_manager()
    
def delete_scene():
    global ACTIVE_MENU
    global MAIN_MENU
    global CREATE_SCENE
    global DELETE_SCENE

    print ()
    print ()
    print ('Scene you want to remove (No Space, AlphaNumeric Only. \'!cancel\' to cancel): ', end='')
    scene = input()
    
    ACTIVE_MENU = MAIN_MENU
    
    if (scene == '!cancel'):
        return
    
    try:
        if os.path.isdir('Scenes/Backups') == False:
            os.mkdir('Scenes/Backups');
            
        copy('Scenes/' + scene + '.cpp', 'Scenes/Backups/' + scene + '.cpp')
        os.remove('Scenes/' + scene + '.cpp')
    except:
        print ('Scene not found!')
        getch()
        
    os.remove('SceneManager.cpp')
    generate_scene_manager()
        
def main():
    global ACTIVE_MENU
    global MAIN_MENU
    global CREATE_SCENE
    global DELETE_SCENE
    
    while True:
        clear()
        
        for i in range(30):
            print()
        
        display_scenes_table()
        
        if ACTIVE_MENU == MAIN_MENU:
            main_menu()
        elif ACTIVE_MENU == CREATE_SCENE:
            create_scene()
        elif ACTIVE_MENU == DELETE_SCENE:
            delete_scene()
            
        sys.stdout.flush()
        
main()
