from time import sleep
import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst

Gst.init(None)

pipeline = Gst.parse_launch("autoaudiosrc ! audioconvert ! queue ! vorbisenc ! oggmux ! filesink location=record.ogg")

pipeline.set_state(Gst.State.PLAYING)

sleep(5)

pipeline.set_state(Gst.State.NULL)
