#ifndef ARDU_ENGINE_H
#define ARDU_ENGINE_H

#include <Arduboy2.h>
#include "ArduObject.h"

class ArduEngine {
  public:
    ArduEngine();
    void Update(Arduboy2 &arduboy);
    void RegisterObject(ArduObject &object);
    void FreedObjects();

  private:
    uint16_t totalObject;
    ArduObject *objects;
};

#endif
