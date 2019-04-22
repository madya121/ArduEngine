from CodeGen import *
import json
import os
import sys
from distutils.dir_util import copy_tree
from shutil import copy

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
            cpp(file[:-4] + ' *' + var + ';')
        
        cpp('')
        
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

    cpp("const unsigned char arduengine_splash[] PROGMEM = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x24, 0x24, 0x18, 0x00, 0xf8, 0x4, 0x4, 0xf8, 0x00, 0xfc, 0x00, 0xf0, 0x00, 0xfc, 0x00, 0xfc, 0x24, 0x24, 0x24, 0x00, 0xfc, 0x24, 0x64, 0xa4, 0x18, 0x00, 0xfc, 0x24, 0x24, 0x24, 0x00, 0xfc, 0x4, 0x4, 0xf8, 0x00, 0x00, 0x00, 0xfc, 0x24, 0x24, 0xd8, 0x00, 0xc, 0x10, 0xe0, 0x10, 0xc, 0x00, 0x00, 0x98, 0x98, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf1, 0xf0, 0x30, 0x30, 0x30, 0x30, 0x31, 0x31, 0x30, 0x30, 0x30, 0x31, 0xf0, 0xf1, 0x00, 0x00, 0x1, 0xf1, 0xf1, 0x31, 0x30, 0x31, 0x30, 0x30, 0x30, 0x31, 0x30, 0x31, 0x31, 0xf1, 0xf1, 0x00, 0x1, 0x1, 0xf1, 0xf0, 0x30, 0x30, 0x30, 0x31, 0x31, 0x31, 0x30, 0x30, 0x30, 0x60, 0xc1, 0x80, 0x00, 0x00, 0x00, 0xf1, 0xf1, 0x30, 0x30, 0xf0, 0xf0, 0x00, 0x00, 0xf0, 0xf0, 0x30, 0x30, 0xf0, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0xcf, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xcf, 0x8f, 0xf, 0xf, 0xf, 0x4f, 0xc0, 0xc0, 0xff, 0x7f, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0x3, 0x87, 0xff, 0xfe, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0x80, 0x80, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0xfc, 0xf9, 0xf3, 0xe7, 0xcf, 0x9f, 0x3f, 0x7f, 0x7f, 0x3f, 0x9f, 0xcf, 0xe7, 0xf3, 0xf9, 0xfc, 0xfe, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x3f, 0x3f, 0x30, 0x30, 0x3f, 0x3f, 0x00, 0x00, 0x3f, 0x3f, 0x30, 0x30, 0x3f, 0x3f, 0x00, 0x00, 0x00, 0x3f, 0x3f, 0x30, 0x30, 0x3f, 0x3f, 0x3, 0x6, 0xc, 0x18, 0x30, 0x31, 0x3f, 0x3f, 0x00, 0x00, 0x00, 0x3f, 0x3f, 0x30, 0x30, 0x33, 0x33, 0x33, 0x33, 0x33, 0x31, 0x30, 0x18, 0xf, 0x7, 0x00, 0x00, 0x00, 0x7, 0xf, 0x1c, 0x38, 0x30, 0x31, 0x33, 0x33, 0x31, 0x30, 0x38, 0x1c, 0xf, 0x7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x3f, 0x9f, 0xcf, 0xe7, 0xf3, 0xf9, 0xfc, 0xfe, 0xff, 0xff, 0xfe, 0xfc, 0xf9, 0xf3, 0xe7, 0xcf, 0x9f, 0x3f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x00, 0x00, 0xfe, 0xfe, 0x1e, 0x1e, 0x1e, 0x1e, 0x1e, 0x78, 0xe0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0xfe, 0x6, 0x6, 0xfe, 0xfe, 0x00, 0x00, 0x00, 0x3e, 0xfe, 0xe6, 0x86, 0x6, 0xe, 0x1e, 0x78, 0xe0, 0x80, 0x00, 0x00, 0x00, 0x80, 0xe0, 0x78, 0x1e, 0x6, 0x6, 0xc6, 0xe6, 0xfe, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xfe, 0xfe, 0xf8, 0xe0, 0x81, 0x7, 0x1e, 0x78, 0xe0, 0x80, 0x80, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3, 0xf, 0x3f, 0xfc, 0xf0, 0xc0, 0x1, 0x7, 0x1e, 0x18, 0x1e, 0x7, 0x1, 0xc0, 0xf0, 0xfc, 0x3f, 0xf, 0x3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0xff, 0xff, 0x1, 0x1, 0x7, 0x1e, 0x78, 0xe0, 0x81, 0x7, 0x1f, 0x7f, 0x7f, 0x00, 0x00, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0xc0, 0xf0, 0x7c, 0x1f, 0x7, 0x1, 0x80, 0xe0, 0x78, 0x1e, 0x6, 0x1e, 0x78, 0xe0, 0x81, 0x7, 0x1f, 0x7e, 0xf8, 0xe0, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x18, 0x18, 0x1f, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1, 0x7, 0x1e, 0x1c, 0x1c, 0x1c, 0x1c, 0x1c, 0x1f, 0x1f, 0x00, 0x00, 0x00, 0x1f, 0x1f, 0x1d, 0x1c, 0x1c, 0x1c, 0x1e, 0x7, 0x1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1, 0x7, 0x1e, 0x1c, 0x1c, 0x1d, 0x1f, 0x1f, 0x1e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};")

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

copy ('ArduEngine.py', 'Projects/{0}/ArduEngine.py'.format(sys.argv[1]))

os.chdir('Projects/{0}/'.format(sys.argv[1]))
os.system('python ArduEngine.py')
