#ifndef ARDU_SPRITE_H
#define ARDU_SPRITE_H

#include <Arduboy2.h>
#include "ArduRect.h"

class ArduSprite : public ArduRect {
  public:
    ArduSprite(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color, const uint8_t *_image):
      ArduRect(_x, _y, _w, _h, _color),
      image(_image)
      {};
    virtual void Update(Arduboy2 &arduboy);

    const uint8_t *image;
};

#endif
