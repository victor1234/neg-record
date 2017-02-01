import pexpect
import time


filname = "record.ogg"
pipeline = "autoaudiosrc ! audioconvert ! queue ! vorbisenc ! oggmux ! filesink location={}".format(filname)

print("running pipeline: {}".format(pipeline))
print("record: 5s")


gstLaunchFilename = "gst-launch-1.0 -e " + pipeline;
gstLaunch = pexpect.spawn(gstLaunchFilename)
time.sleep(5)
gstLaunch.sendcontrol('c')
print(gstLaunch.before)




