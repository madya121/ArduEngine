#include "ArduSprite.h"

void ArduSprite::Update(Arduboy2 &arduboy) {
  if (!isEnabled)
    return;

  arduboy.drawBitmap(x, y, image, w, h, color);
}
