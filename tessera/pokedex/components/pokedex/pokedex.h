#pragma once
#include "esphome/core/component.h"
#include "esphome/components/smart_display/plugin_api.h"

namespace esphome::pokedex {

class DexSaver;

// The plugin: an ESPHome component and a tessera::Plugin. It registers its screensaver in setup(), and hands the
// answers of the app (the dex entry the saver asked for) to the saver on the glass.
class Pokedex : public Component, public tessera::Plugin {
 public:
  void setup() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void on_message(JsonObjectConst message) override;
  // The saver on the glass, or none: it says so itself when it comes and goes.
  void attach(DexSaver *saver) { shown_ = saver; }
  void detach(DexSaver *saver) {
    if (shown_ == saver) shown_ = nullptr;
  }

 private:
  DexSaver *shown_ = nullptr;
};

}  // namespace esphome::pokedex
