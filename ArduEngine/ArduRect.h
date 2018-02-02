#ifndef ARDU_RECT_H
#define ARDU_RECT_H

#include <Arduboy2.h>
#include "ArduObject.h"

class ArduRect : public ArduObject {
  public:
    ArduRect();
    ArduRect(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color):
      ArduObject(), x(_x), y(_y), w(_w), h(_h), color(_color), isFill(false) {};
    virtual void Update(Arduboy2 &arduboy);

    int16_t x, y;
    int16_t w, h;
    uint8_t color;
    bool isFill;
};

#endif
