#ifndef ARDU_ENGINE_H
#define ARDU_ENGINE_H

#include <Arduboy2.h>
#include <string.h>

class ArduObject;
class ArduScene;

class ArduCamera {
  public:
    ArduCamera(): x(0), y(0) {};
    void WorldToCameraPosition(int16_t _x, int16_t _y, int16_t *outX, int16_t *outY);

    int16_t x, y;
};

class ArduEngine {
  public:
    ArduEngine(Arduboy2 &arduboy);
    void Update(Arduboy2 &arduboy);
    void RegisterObject(ArduObject &object);
    void FreedObjects();
    void RegisterScene(ArduScene &scene);
    void FreedScenes();
    void SetScene(uint8_t sceneID);
    ArduCamera* GetCamera();

    Arduboy2 *arduboy;

  private:
    uint8_t totalObject;
    uint8_t totalScene;

    ArduObject **objects;
    ArduScene **scenes;

    uint8_t currentObjectLimit;
    uint8_t currentSceneLimit;

    ArduScene *currentScene;

    ArduCamera *camera;
};

class ArduScene {
  public:
    ArduScene(uint8_t _sceneID, ArduEngine &engine): sceneID(_sceneID) {
      engine.RegisterScene(*this);
    };
    virtual void Load(ArduEngine &engine) {};
    virtual void Run(ArduEngine &engine) {};
    virtual void Destroy(ArduEngine &engine) {};

    uint8_t sceneID;
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
    ArduRect(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color, ArduEngine &engine):
      ArduObject(), x(_x), y(_y), w(_w), h(_h), color(_color), isFill(false) {
        engine.RegisterObject(*this);
      };
    virtual void Update(ArduEngine &engine);

    int16_t x, y;
    int16_t w, h;
    uint8_t color;
    bool isFill;
};

class ArduSprite : public ArduRect {
  public:
    ArduSprite(int16_t _x, int16_t _y, int16_t _w, int16_t _h, uint8_t _color, const uint8_t *_image, ArduEngine &engine):
      ArduRect(_x, _y, _w, _h, _color, engine),
      image(_image) {};
    virtual void Update(ArduEngine &engine);

    const uint8_t *image;
};

class ArduText : public ArduObject {
  public:
    ArduText(int16_t _x, int16_t _y, const char *_text, ArduEngine &engine);
    virtual void Update(ArduEngine &engine);
    void SetText(const char *_text);
    void SetText(int16_t _number);
    void SetSize(uint8_t _size);
    void SetPosition(int16_t _x, int16_t _y);

  private:
    int16_t x, y;
    uint8_t size;
    char text[64];
};

#endif
