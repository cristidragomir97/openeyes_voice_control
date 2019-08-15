#!/usr/bin/env python

"""This module is a simple demonstration of voice control
for ROS turtlebot using pocketsphinx
"""

import argparse
import roslib
import rospy

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio

model = 'en-us'
lexicon = 'voice_cmd.dict' 
kwlist = 'en-us.lm.bin'


if __name__ == '__main__':
        config = Decoder.default_config()
        config.set_string('-hmm', model)
        config.set_string('-dict', lexicon)
        config.set_string('-lm', kwlist)

        decoder = Decoder(config)

        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        in_speech_bf = False
        decoder.start_utt()
        while True:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, False, False)
                if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                        decoder.end_utt()
                        print('Result:', decoder.hyp().hypstr)
                        decoder.start_utt()
            else:
                break
        decoder.end_utt()