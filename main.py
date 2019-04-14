from CodeGen import *
import json
import os
import sys
from distutils.dir_util import copy_tree

def generate_scene_id(name):
    result = '';
    for c in name:
        if c.isupper():
            result = result + '_'
        result = result + c.upper()
    
    return result[1:] + '_SCENE_ID'
    
def generate_scene_variable(name):
    return name[:1].lower() + name[1:-4]
        

def generate_scene_manager(path, game_name):
    files = os.listdir('Projects/' + game_name + '/Scenes/')

    cpp = CppFile(path + 'SceneManager.cpp')
    cpp('#ifndef SCENE_MANAGER_CPP')
    cpp('#define SCENE_MANAGER_CPP')
    
    cpp('')
    
    for file in files:
        cpp('#include "Scenes/' + file + '"')
    
    cpp('')
    
    for i in range(len(files)):
        id = generate_scene_id(files[i][:-4])
        cpp('const uint8_t ' + id + ' = ' + str(i) + ';')
    
    cpp('')
    
    with cpp.block('class SceneManager', ';'):
        cpp.label('public')
        
        for file in files:
            var = generate_scene_variable(file)
            cpp(file[:-4] + ' *' + var + ';\n')
        
        with cpp.block('SceneManager(ArduEngine &engine)'):
            
            for file in files:
                var = generate_scene_variable(file)
                id  = generate_scene_id(file[:-4])
                cpp(var + ' = new ' + file[:-4] + '(engine, ' + id + ');')
    
    cpp('#endif')
    cpp.close()

def generate_game_scene(path, scene_name):
    cpp = CppFile(path + scene_name + '.cpp')
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

def generate_main_ino(path, game_name):
    cpp = CppFile(path + game_name + '.ino')

    # Includes
    cpp('#include <Arduboy2.h>')
    cpp('#include <ArduboyTones.h>')
    cpp('')
    cpp('#include "ArduEngine/ArduRect.cpp"')
    cpp('#include "ArduEngine/ArduSprite.cpp"')
    cpp('#include "ArduEngine/ArduText.cpp"')
    cpp('#include "ArduEngine/ArduEngine.cpp"')
    cpp('')
    cpp('#include "SceneManager.cpp"')
    cpp('')
    cpp('#include "Images.h"')
    cpp('')

    # Declarations
    cpp('Arduboy2 arduboy;')
    cpp('ArduboyTones sound(arduboy.audio.enabled);')
    cpp('ArduEngine *arduEngine = new ArduEngine(arduboy);')
    cpp('')
    cpp('SceneManager *sceneManager = new SceneManager(*arduEngine);')

    cpp('')
    with cpp.block('void setup()'):
        cpp('arduboy.begin();')
        cpp('arduboy.setFrameRate(30);')
        cpp('arduboy.initRandomSeed();\n')
        cpp('arduEngine->SetScene(SPLASH_SCREEN_SCENE_ID);')

    cpp('')
    with cpp.block('void loop()'):
        cpp('if (!(arduboy.nextFrame())) return;')
        cpp('arduboy.pollButtons();')
        cpp('arduboy.clear();\n')
        cpp('arduEngine->Update(arduboy);\n')
        cpp('arduboy.display();')

    cpp.close()

def generate_scene_id_file(path):
    cpp = CppFile(path + 'SceneID.h')

    cpp('#ifndef SCENE_ID_H')
    cpp('#define SCENE_ID_H\n')

    cpp('const uint8_t SPLASH_SCREEN_SCENE_ID = 1;')

    cpp('\n#endif')
    cpp.close()

def generate_image_file(path):
    cpp = CppFile(path + 'Images.h')

    cpp('#ifndef IMAGES_H')
    cpp('#define IMAGES_H\n')

    cpp("const unsigned char arduengine_splash[] PROGMEM = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x80, 0xc0, 0xc0, 0x60, 0x20, 0x30, 0x30, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x10, 0x10, 0x30, 0x60, 0xc0, 0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0x1c, 0x6, 0x43, 0xa1, 0x50, 0x00, 0xf8, 0xc, 0x6, 0x23, 0x11, 0xc9, 0xc8, 0xc8, 0x00, 0x00, 0x00, 0xc8, 0xc9, 0xc9, 0x13, 0x26, 0xc, 0xf8, 0x00, 0x3, 0xe, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1, 0x1f, 0xf0, 0x81, 0x2, 0x21, 0xf0, 0x23, 0x66, 0xcc, 0x98, 0xf0, 0x1, 0x1, 0xe1, 0x8, 0xc, 0xe0, 0x1, 0x1, 0xf1, 0x98, 0xcc, 0x46, 0x63, 0x30, 0x18, 0xc, 0x7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1, 0x3, 0x1, 0x1, 0x00, 0x00, 0x00, 0x00, 0x7, 0x4, 0x4, 0x7, 0x4, 0x4, 0x7, 0x4, 0x4, 0x7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x1, 0x1, 0x79, 0x49, 0x9, 0x9, 0xff, 0x00, 0x00, 0xff, 0x1, 0x1, 0x95, 0x11, 0x11, 0xff, 0x00, 0x00, 0xcf, 0x49, 0x79, 0x1, 0x1, 0x79, 0x49, 0xcf, 0x00, 0x00, 0xff, 0x1, 0x3, 0xe6, 0x44, 0xe6, 0x3, 0x1, 0xff, 0x00, 0x00, 0x00, 0x00, 0xff, 0x1, 0x1, 0xc1, 0x49, 0x41, 0x41, 0x7f, 0x00, 0x00, 0xff, 0x1, 0x1, 0x95, 0x11, 0x11, 0xff, 0x00, 0x00, 0xff, 0x1, 0x1, 0x79, 0x79, 0x1, 0x1, 0xff, 0x00, 0x00, 0xff, 0x41, 0x41, 0x49, 0x9, 0x9, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x3, 0x00, 0x00, 0x3, 0x2, 0x2, 0x3, 0x2, 0x2, 0x3, 0x00, 0x00, 0x3, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x3, 0x00, 0x00, 0x3, 0x2, 0x2, 0x3, 0x00, 0x3, 0x2, 0x2, 0x3, 0x00, 0x00, 0x00, 0x00, 0x3, 0x2, 0x2, 0x3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3, 0x2, 0x2, 0x3, 0x2, 0x2, 0x3, 0x00, 0x00, 0x3, 0x2, 0x2, 0x2, 0x2, 0x2, 0x2, 0x3, 0x00, 0x00, 0x3, 0x2, 0x2, 0x2, 0x2, 0x2, 0x3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};")

    cpp('\n#endif')
    cpp.close()



def create_new_game(game_name):
    if os.path.isdir('Projects') == False:
        os.mkdir('Projects');
        
    if os.path.isdir('Projects/' + game_name):
        print ('{0} is already exist'.format(game_name))
    else:
        print ('Create folder {0}...'.format(game_name))
        os.mkdir('Projects/' + game_name)
        
        print ('Generate .ino file for {0}...'.format(game_name))
        generate_main_ino('Projects/' + game_name + '/', game_name)
        
        print ('Copying ArduEngine library into {0}...'.format(game_name))
        copy_tree("ArduEngine", 'Projects/' + game_name + "/ArduEngine")
        
        print ('Add Sample Splash Screen Scene')
        os.mkdir('Projects/' + game_name + '/Scenes');
        generate_game_scene('Projects/' + game_name + '/Scenes/', 'SplashScreen')
        
        generate_image_file('Projects/' + game_name + '/')
        # generate_scene_id_file('Projects/' + game_name + '/')
        generate_scene_manager('Projects/' + game_name + '/', game_name);
        
        print ('{0} is ready to develop!'.format(game_name))

# add_game_scene('MainMenu')
# generate_main_ino('GameSomething')
create_new_game(sys.argv[1])
# generate_game_scene('Scene');
