#ifndef ARDU_TEXT_CPP
#define ARDU_TEXT_CPP

#include <string.h>

#include "ArduEngine.h"

ArduText::ArduText(int16_t _x, int16_t _y, const char *_text, ArduEngine &engine): ArduObject(engine) {
  this->x = _x;
  this->y = _y;

  this->size = 1;
  strcpy (this->text, _text);
}

void ArduText::Update(ArduEngine &engine) {
  if (!isEnabled)
    return;

  engine.arduboy->setCursor(x, y);
  engine.arduboy->setTextSize(size);
  engine.arduboy->print(text);
}

void ArduText::SetPosition(int16_t _x, int16_t _y) {
  this->x = _x;
  this->y = _y;
}

void ArduText::SetSize(uint8_t _size) {
  this->size = _size;
}

void ArduText::SetText(const char *_text) {
  strcpy (this->text, _text);
}

void ArduText::SetText(int16_t _number) {
  sprintf (this->text, "%d", _number);
}

#endif
