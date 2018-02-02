#ifndef ARDU_ENGINE_CPP
#define ARDU_ENGINE_CPP

#include "ArduEngine.h"

ArduEngine::ArduEngine() {
  totalObject = 0;
  objects = new ArduObject();

  totalScene = 0;
  scenes = new ArduScene();
}

void ArduEngine::Update(Arduboy2 &arduboy) {
  for (uint16_t i = 0; i < totalObject; i++)
    (objects + i)->Update(arduboy);
}

void ArduEngine::RegisterObject(ArduObject &object) {
  *(objects + totalObject) = object;
  totalObject++;
}

void ArduEngine::FreedObjects() {
  for (uint16_t i = 0; i < totalObject; i++)
    delete (objects + i);
  totalObject = 0;
}

void ArduEngine::RegisterScene(ArduScene &scene) {
  *(scenes + totalScene) = scene;
  totalScene++;
}

void ArduEngine::FreedScenes() {
  for (uint16_t i = 0; i < totalScene; i++)
    delete (scenes + i);
  totalScene = 0;
}

#endif
