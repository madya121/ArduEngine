#ifndef ARDU_CAMERA_CPP
#define ARDU_CAMERA_CPP

#include "ArduEngine.h"

void ArduCamera::WorldToCameraPosition(int16_t _x, int16_t _y, int16_t *outX, int16_t *outY) {
  *outX = _x - this->x;
  *outY = _y - this->y;
}

#endif
