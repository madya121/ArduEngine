#ifndef ARDU_ENGINE_H
#define ARDU_ENGINE_H

#include <Arduboy2.h>
#include "ArduObject.h"
#include "ArduScene.h"

class ArduEngine {
  public:
    ArduEngine();
    void Update(Arduboy2 &arduboy);
    void RegisterObject(ArduObject &object);
    void FreedObjects();
    void RegisterScene(ArduScene &scene);
    void FreedScenes();

  private:
    uint16_t totalObject;
    uint16_t totalScene;

    ArduObject *objects;
    ArduScene *scenes;
};

#endif
