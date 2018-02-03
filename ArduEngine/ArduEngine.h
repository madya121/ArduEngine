#ifndef ARDU_ENGINE_H
#define ARDU_ENGINE_H

#include <Arduboy2.h>

class ArduObject;
class ArduScene;

class ArduEngine {
  public:
    ArduEngine(Arduboy2 &arduboy);
    void Update(Arduboy2 &arduboy);
    void RegisterObject(ArduObject &object);
    void FreedObjects();
    void RegisterScene(ArduScene &scene);
    void FreedScenes();

    Arduboy2 *arduboy;

  private:
    uint16_t totalObject;
    uint16_t totalScene;

    ArduObject **objects;
    ArduScene **scenes;

    uint16_t currentObjectLimit;
    uint16_t currentSceneLimit;
};

class ArduScene {
  public:
    ArduScene() {};
    virtual void PreScene(ArduEngine &engine) {};
    virtual void Scene(ArduEngine &engine) {};
};

class ArduObject {
  public:
    ArduObject(): isEnabled(true) {};
    virtual void Update(ArduEngine &engine) {};

    bool isEnabled;
};

class ArduRect : public ArduObject {
  public:
    ArduRect();
    ArduRect(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color):
      ArduObject(), x(_x), y(_y), w(_w), h(_h), color(_color), isFill(false) {};
    virtual void Update(ArduEngine &engine);

    int16_t x, y;
    int16_t w, h;
    uint8_t color;
    bool isFill;
};

class ArduSprite : public ArduRect {
  public:
    ArduSprite(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color, const uint8_t *_image):
      ArduRect(_x, _y, _w, _h, _color),
      image(_image)
      {};
    virtual void Update(ArduEngine &engine);

    const uint8_t *image;
};

#endif
