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
}

void ArduEngine::Update(Arduboy2 &arduboy) {
  for (uint16_t i = 0; i < totalObject; i++) {
    objects[i]->Update(*this);
  }
  for (uint16_t i = 0; i < totalScene; i++) {
    scenes[i]->Scene(*this);
  }
}

void ArduEngine::RegisterObject(ArduObject &object) {
  if (totalObject == currentObjectLimit) {
    ArduObject **arrObject = new ArduObject* [currentObjectLimit + ARR_LIMIT];

    for (uint16_t i = 0; i < totalObject; i++)
      arrObject[i] = objects[i];

    objects = arrObject;
    currentObjectLimit += ARR_LIMIT;
  }
  objects[totalObject] = &object;
  totalObject++;
}

void ArduEngine::FreedObjects() {
  for (uint16_t i = 0; i < totalObject; i++)
    delete (objects + i);
  totalObject = 0;
}

void ArduEngine::RegisterScene(ArduScene &scene) {
  if (totalScene == currentSceneLimit) {
    ArduScene  **arrScene = new ArduScene*[currentSceneLimit + ARR_LIMIT];

    for (uint16_t i = 0; i < totalScene; i++)
      arrScene[i] = scenes[i];

    scenes = arrScene;
    currentSceneLimit += ARR_LIMIT;
  }
  scenes[totalScene] = &scene;
  totalScene++;
}

void ArduEngine::FreedScenes() {
  for (uint16_t i = 0; i < totalScene; i++)
    delete (scenes + i);
  totalScene = 0;
}

#endif
