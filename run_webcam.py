import argparse
import logging
import time
import sys
import cv2
import numpy as np
import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

import ctcsound
cs = ctcsound.Csound()

csd = '''
<CsoundSynthesizer>

<CsOptions>
  -d -o dac -m0
</CsOptions>

<CsInstruments>
sr     = 48000
ksmps  = 100
nchnls = 2
0dbfs  = 1

          instr 1
idur      =         p3
iamp      =         p4
icps      =         cpspch(p5)
irise     =         p6
idec      =         p7
ipan      =         p8

kenv      linen     iamp, irise, idur, idec
kenv      =         kenv*kenv
asig      poscil    kenv, icps
a1, a2    pan2      asig, ipan
          outs      a1, a2
          endin
</CsInstruments>

<CsScore>
f 0 14400    ; a 4 hours session should be enough
</CsScore>
</CsoundSynthesizer>
'''
cs.compileCsdText(csd)
cs.start()

pt = ctcsound.CsoundPerformanceThread(cs.csound())
pt.play()

# logger = logging.getLogger('TfPoseEstimator-WebCam')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

fps_time = 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()

    # logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    # logger.debusg('cam read+')
    cam = cv2.VideoCapture(args.camera)
    ret_val, image = cam.read()
    # logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))

    while True:
        ret_val, image = cam.read()

        # logger.debug('image process+')
    
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
  
        if (len(humans) > 0 ):
            if (humans[0].body_parts.get(16)) :
                body_part = humans[0].body_parts.get(16)
                X = body_part.x
                Y = body_part.y       
                #print(X)
                PoseMax = 0.6
                PoseMin = 0.3
                AudioMax = 8.5
                AudioMin = 6.0 
                PoseRange = (PoseMax - PoseMin)  
                AudioRange = (AudioMax - AudioMin)  
                NewValue = (((X - PoseMin) * AudioRange) / PoseRange) + AudioMin
                #print(NewValue)
                pt.scoreEvent(False, 'i', (1, 0.5, 1, 0.5, NewValue,  0.05, 0.3, 0.5))
                #pt.scoreEvent(False, 'i', (1, 0.5, 1, 0.5, 9.06, 0.05, 0.3, 0.5))
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        # logger.debug('show+')
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        # logger.debug('finished+')

    cv2.destroyAllWindows()
    pt.stop()
    pt.join()
    sys.exit(0)
    
