#ifndef ARDU_SCENE_H
#define ARDU_SCENE_H

#include <Arduboy2.h>

class ArduScene {
  public:
    ArduScene() {};
    virtual void PreScene(Arduboy2 &arduboy) {};
    virtual void Scene(Arduboy2 &arduboy) {};
};

#endif
