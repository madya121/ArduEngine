#ifndef ARDU_SPRITE_CPP
#define ARDU_SPRITE_CPP

#include "ArduEngine.h"

void ArduSprite::Update(ArduEngine &engine) {
  if (!isEnabled)
    return;

  engine.arduboy->drawBitmap(x, y, image, w, h, color);
}

#endif
