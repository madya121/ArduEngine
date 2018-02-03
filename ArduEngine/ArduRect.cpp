#ifndef ARDU_RECT_CPP
#define ARDU_RECT_CPP

#include "ArduEngine.h"

void ArduRect::Update(ArduEngine &engine) {
  if (!isEnabled)
    return;

  if (!isFill)
    engine.arduboy->drawRect(x, y, w, h, color);
  else
    engine.arduboy->fillRect(x, y, w, h, color);
}

#endif
