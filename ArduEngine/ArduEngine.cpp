#include "ArduEngine.h"

ArduEngine::ArduEngine() {
  totalObject = 0;
  objects = new ArduObject();
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
