# https://github.com/gluon/AbletonLive12_MIDIRemoteScripts/blob/main/ableton/v2/control_surface/components/session_ring.py

from ableton.v2.control_surface.components.session_ring import SessionRingComponent
from functools import partial
from typing import Optional, Tuple, Any
import logging
from .handler import AbletonOSCHandler

import Live

logger = logging.getLogger("abletonosc")

class SessionRingHandler(AbletonOSCHandler):
  def __init__(self, manager):
    self.session_ring = SessionRingComponent(num_tracks = 8, num_scenes = 1)
    self.session_ring.set_enabled(False)
    super().__init__(manager)
    self.class_identifier = "session_ring"

  def init_api(self):
    #--------------------------------------------------------------------------------
    # Callbacks for session_ring: methods
    #--------------------------------------------------------------------------------
    for method in []:
      callback = partial(self._call_method, self.session_ring, method)
      self.osc_server.add_handler("/live/session_ring/%s" % method, callback)

    #--------------------------------------------------------------------------------
    # Callbacks for session_ring: properties (read/write)
    #--------------------------------------------------------------------------------
    properties_rw = []

    #--------------------------------------------------------------------------------
    # Callbacks for session_ring: properties (read-only)
    #--------------------------------------------------------------------------------
    properties_r = [
      "num_tracks",
      "num_scenes",
      "track_offset",
      "scene_offset"
    ]

    for prop in properties_r + properties_rw:
      self.osc_server.add_handler("/live/session_ring/get/%s" % prop, partial(self._get_property, self.session_ring, prop))
      self.osc_server.add_handler("/live/session_ring/start_listen/%s" % prop, partial(self._start_listen, self.session_ring, prop))
      self.osc_server.add_handler("/live/session_ring/stop_listen/%s" % prop, partial(self._stop_listen, self.session_ring, prop))
    for prop in properties_rw:
      self.osc_server.add_handler("/live/session_ring/set/%s" % prop, partial(self._set_property, self.session_ring, prop))

    def set_num_tracks(params: Tuple[Any] = ()):
      num_tracks, = params
      self.session_ring._session_ring.num_tracks = int(num_tracks)
      self.session_ring.on_enabled_changed()
    self.osc_server.add_handler("/live/session_ring/set/num_tracks", set_num_tracks)

    def set_num_scenes(params: Tuple[Any] = ()):
      num_scenes, = params
      self.session_ring._session_ring.num_scenes = int(num_scenes)
      self.session_ring.on_enabled_changed()
    self.osc_server.add_handler("/live/session_ring/set/num_scenes", set_num_scenes)

    def set_track_offset(params: Tuple[Any] = ()):
      track_offset, = params
      self.session_ring._session_ring.track_offset = int(track_offset)
      self.session_ring.on_enabled_changed()
    self.osc_server.add_handler("/live/session_ring/set/track_offset", set_track_offset)

    def set_scene_offset(params: Tuple[Any] = ()):
      scene_offset, = params
      self.session_ring._session_ring.scene_offset = int(scene_offset)
      self.session_ring.on_enabled_changed()
    self.osc_server.add_handler("/live/session_ring/set/scene_offset", set_scene_offset)

    def get_coordinates(params: Tuple[Any] = ()):
      logger.info("get coordinates")
      return self.session_ring.track_offset, self.session_ring.scene_offset, self.session_ring.num_tracks, self.session_ring.num_scenes
    self.osc_server.add_handler("/live/session_ring/get/coordinates", get_coordinates)

    def get_enabled(params: Tuple[Any] = ()):
      return self.session_ring.is_enabled(),
    self.osc_server.add_handler("/live/session_ring/get/enabled", get_enabled)

    def set_enabled(params: Tuple[Any] = ()):
      enabled, = params
      self.session_ring.set_enabled(bool(enabled))
    self.osc_server.add_handler("/live/session_ring/set/enabled", set_enabled)

    def move(params: Tuple[Any] = ()): # tracks_increment, scenes_increment, e.g. 0, +1
      tracks, scenes = params
      move = True
      if self.session_ring.track_offset + tracks < 0:
        move = False
      if self.session_ring.scene_offset + scenes < 0:
        move = False
      if (tracks != 0) and (self.session_ring.track_offset + self.session_ring.num_tracks + tracks > len(self.song.tracks)):
        move = False
      if self.session_ring.scene_offset + self.session_ring.num_scenes + scenes > len(self.song.scenes):
        move = False

      if move:
        self.session_ring.move(int(tracks), int(scenes))
    self.osc_server.add_handler("/live/session_ring/move", move)

    def set_offsets(params: Tuple[Any] = ()): # new track offset, new scene offset, e.g. 0, 3
      tracks, scenes = params
      self.session_ring.set_offsets(int(tracks), int(scenes))
    self.osc_server.add_handler("/live/session_ring/set_offsets", set_offsets)

    add_scene_offset_listener = ''
  # __events__ = ('offset', 'tracks')