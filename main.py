from CodeGen import *
import json
import os
import sys
from distutils.dir_util import copy_tree

# TODO: Work on Game Scene
'''
def add_game_scene(scene_name):
    config = {}
    game_states = []
    with open('config.json') as json_data:
        config = json.load(json_data)
        game_states = config['game_states']

    for state in game_states:
        if scene_name == state:
            raise Exception('Scene was already defined')

    game_states.append(scene_name)
    config['game_states'] = game_states

    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)
'''

# TODO: Work On Game Scene
'''
def refresh_game_state():
    config = {}
    game_states = []
    with open('config.json') as json_data:
        config = json.load(json_data)
        game_states = config['game_states']

    cpp = CppFile('GameState.h')
    cpp('/****************************')
    cpp(' ** THIS FILE IS GENERATED **')
    cpp(' ****************************/\n')

    cpp('#ifndef GAME_STATE_H')
    cpp('#define GAME_STATE_H\n')

    index = 0
    for state in game_states:
        with cpp.subs(name=state.upper(), i=index):
            cpp('#define $name$_PRE_SCENE $i$;')
            index += 1
        with cpp.subs(name=state.upper(), i=index):
            cpp('#define $name$_SCENE $i$; \n')
            index += 1
        with cpp.block('void GoTo' + state + '()'):
            cpp('return;')

    cpp('\n#endif')
    cpp.close()
'''

def generate_global(path):
    cpp = CppFile(path + 'Global.h')
    cpp('#ifndef GLOBAL_H')
    cpp('#define GLOBAL_H\n')

    # Includes
    cpp('#include <Arduboy2.h>')
    cpp('#include <ArduboyTones.h>')

    cpp('')

    cpp('#include "ArduEngine/ArduObject.h"')
    cpp('#include "ArduEngine/ArduRect.cpp"')
    cpp('#include "ArduEngine/ArduSprite.cpp"')
    cpp('#include "ArduEngine/ArduEngine.cpp"')

    cpp('')

    # Declarations
    cpp('Arduboy2 arduboy;')
    cpp('ArduboyTones sound(arduboy.audio.enabled);')
    cpp('ArduEngine arduEngine = new ArduEngine();')

    cpp('\n#endif')
    cpp.close()

def generate_main_ino(path, game_name):
    cpp = CppFile(path + game_name + '.ino')

    cpp('#include "Global.h"\n')

    with cpp.block('void InitializeScenes();'):
        cpp('// TODO: Add example scene here')

    cpp('')
    with cpp.block('void setup()'):
        cpp('arduboy.begin();')
        cpp('arduboy.setFrameRate(60);')
        cpp('arduboy.initRandomSeed();\n')
        cpp('InitializeScenes()')

    cpp('')
    with cpp.block('void loop()'):
        cpp('if (!(arduboy.nextFrame())) return;')
        cpp('arduboy.pollButtons();')
        cpp('arduboy.clear();\n')
        cpp('arduEngine.Update(arduboy);\n')
        cpp('arduboy.display();')

    cpp.close()

def create_new_game(game_name):
    if os.path.isdir(game_name):
        print ('{0} is already exist'.format(game_name))
    else:
        print ('Create folder {0}...'.format(game_name))
        os.mkdir(game_name)
        print ('Generate .ino file for {0}...'.format(game_name))
        generate_main_ino(game_name + '/', game_name)
        print ('Generate Global file...')
        generate_global(game_name + '/')
        print ('Copying ArduEngine library into {0}...'.format(game_name))
        copy_tree("ArduEngine", game_name + "/ArduEngine")
        print ('{0} is ready to develop!'.format(game_name))

# add_game_scene('MainMenu')
# generate_main_ino('GameSomething')
create_new_game(sys.argv[1])
