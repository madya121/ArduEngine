#ifndef ARDU_SPRITE_CPP
#define ARDU_SPRITE_CPP

#include "ArduSprite.h"

void ArduSprite::Update(Arduboy2 &arduboy) {
  if (!isEnabled)
    return;

  arduboy.drawBitmap(x, y, image, w, h, color);
}

#endif
