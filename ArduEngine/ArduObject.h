#ifndef ARDU_OBJECT_H
#define ARDU_OBJECT_H

#include <Arduboy2.h>

class ArduObject {
  public:
    ArduObject(): isEnabled(true) {};
    virtual void Update(Arduboy2 &arduboy);

    bool isEnabled;
};

#endif
