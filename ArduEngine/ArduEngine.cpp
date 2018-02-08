#ifndef ARDU_ENGINE_CPP
#define ARDU_ENGINE_CPP

#include "ArduEngine.h"

#define ARR_LIMIT 5

ArduEngine::ArduEngine(Arduboy2 &arduboy) {
  totalObject = 0;
  totalScene = 0;

  ArduObject **arrObject = new ArduObject* [5];
  ArduScene  **arrScene = new ArduScene* [5];

  objects = arrObject;
  scenes = arrScene;

  currentObjectLimit = ARR_LIMIT;
  currentSceneLimit  = ARR_LIMIT;

  this->arduboy = &arduboy;

  currentScene = NULL;
}

void ArduEngine::Update(Arduboy2 &arduboy) {
  for (uint8_t i = 0; i < totalObject; i++) {
    objects[i]->Update(*this);
  }

  if (currentScene != NULL) {
    currentScene->Run(*this);
  }
}

void ArduEngine::SetScene(uint8_t sceneID) {
  if (currentScene != NULL) {
    currentScene->Destroy(*this);
  }

  for (uint8_t i = 0; i < totalScene; i++) {
    if (scenes[i]->sceneID == sceneID) {
      currentScene = scenes[i];
      break;
    }
  }

  if (currentScene != NULL) {
    currentScene->Load(*this);
  }
}

void ArduEngine::RegisterObject(ArduObject &object) {
  if (totalObject == currentObjectLimit) {
    ArduObject **arrObject = new ArduObject* [currentObjectLimit + ARR_LIMIT];

    for (uint8_t i = 0; i < totalObject; i++)
      arrObject[i] = objects[i];

    objects = arrObject;
    currentObjectLimit += ARR_LIMIT;
  }
  objects[totalObject] = &object;
  totalObject++;
}

void ArduEngine::FreedObjects() {
  for (uint8_t i = 0; i < totalObject; i++)
    delete (objects + i);
  totalObject = 0;
}

void ArduEngine::RegisterScene(ArduScene &scene) {
  if (totalScene == currentSceneLimit) {
    ArduScene  **arrScene = new ArduScene*[currentSceneLimit + ARR_LIMIT];

    for (uint8_t i = 0; i < totalScene; i++)
      arrScene[i] = scenes[i];

    scenes = arrScene;
    currentSceneLimit += ARR_LIMIT;
  }
  scenes[totalScene] = &scene;
  totalScene++;
}

void ArduEngine::FreedScenes() {
  for (uint8_t i = 0; i < totalScene; i++)
    delete (scenes + i);
  totalScene = 0;
}

#endif
