from kivy.core.audio import Sound

from configurables import userSettings
from lib.betterLogger import BetterLogger


class Audio(BetterLogger):
    __log_name__ = "Audio"
    _audios: dict[str, Sound] = {}
    current_playing: Sound = None

    def register(self, name: str, audio: Sound):
        self.log_deep_debug("Registering audio", audio, "for", name)

        audio.volume = userSettings.get("UI", "volume")
        self._audios[name] = audio

    def get(self, name: str) -> Sound:
        return self._audios[name]

    def loop(self, name: str):
        self.log_deep_debug("Looping", name)

        if self.current_playing is not None:
            self.current_playing.stop()

        self.current_playing = self._audios[name]
        self.current_playing.play()
        self.current_playing.bind(on_stop=lambda _instance: self.loop_restart())

    def loop_restart(self):
        self.current_playing.play()


Audio: Audio = Audio()


__all__ = ["Audio"]
