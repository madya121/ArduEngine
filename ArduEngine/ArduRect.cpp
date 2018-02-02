#include "ArduRect.h"

void ArduRect::Update(Arduboy2 &arduboy) {
  if (!isEnabled)
    return;

  if (!isFill)
    arduboy.drawRect(x, y, w, h, color);
  else
    arduboy.fillRect(x, y, w, h, color);
}
