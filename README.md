# ArduEngine
Simple Arduboy Scene Management Framework

## Getting Started
1. Clone / Fork the project
2. Install from Python official website
```
https://www.python.org/downloads
```
3. From your Terminal / Command Prompt, go to `ArduEngine` project and run this command below. (Note that your project name must be Alphanumeric only and without space)
```
python ./main.py [Your Project Name]
```
4. Your project will be created under `/Projects` directory and your terminal will be showing `ArduEngine` Window

## ArduEngine Window
This tool manages your scenes and removes boilerplate while creating a new scene for yor game.

[IMG]

1. List of your scenes
2. Press 1 if you want to create a new scene
3. Press 2 if you want to remove a scene
4. Rebuild the SceneManager from your available scenes.

Your scenes will be located under `[Your Project]/Scenes`. `SceneManager` will read this folder and generate a code that contains every scene id and initializing your scenes.
Because of this, it's not recommended to edit `SceneManager` manually, unless you know what you're doing.

### Create New Scene
1. Press 1 on `ArduEngine` Window.
2. Enter your scene name (Must be Alphanumeric and no space) then press enter.
3. Your new scene will be created under the `/Scenes` folder and `SceneManager` will be updated.

### Remove Scene
1. Press 2 on Arduengine Window.
2. Enter your scene name that you want to remove.
3. Your scene will be moved to /Scenes/Backups directory and your SceneManager will be updated.

It's recommended to create and remove scene from the `ArduEngine` Window instead of doing it manually. If somehow you create a new scene manually, you have to put your scene under the `/Scenes` folder, then you can rebuild the `SceneManager` from the window.

Every scenes inside the `/Backups` folder are safe to delete.

## ArduEngine Project Structure
```
/YourProjectName
    /ArduEngine         # ArduEngine Library
    /Scenes             # All of your scenes are located here
    
    ArduEngine.py       # This is an ArduEngine Window Script. Open ArduEngine Window with this command "python ./ArduEngine.py"
    Images.h            # Put all of your images here
    SceneManager.cpp
    YourProjectName.ino # Your main code
```

## Set Scene
To set the first scene to be shown when the game is turned on, go to your `YourProjectName.ino` file, and look inside the `setup()` method. You will find `arduEngine->SetScene(SPLASH_SCREEN_SCENE_ID);`. After you create some other scenes, change the `SPLASH_SCREEN_SCENE_ID` into your scene ID defined inside the `SceneManager.cpp`.

To change the scene from your scene, once you have the `&arduEngine` object, you can use `arduEngine.SetScene(YOUR_SCENE_ID)` to change into a different scene.

## Other Things
Go to [Wiki](https://github.com/madya121/ArduEngine/wiki) to find out more what is inside the `ArduEngine`

