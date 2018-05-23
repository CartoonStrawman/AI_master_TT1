
import numpy as np  
import os  
import six.moves.urllib as urllib  
import sys  
import tarfile  
import tensorflow as tf  
import zipfile  
import cv2

from collections import defaultdict  
from io import StringIO  
from matplotlib import pyplot as plt  
from PIL import Image  
from utils import label_map_util
from utils import visualization_utils as vis_util

def main(_):
    NUM_CLASSES = 2

    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      #with tf.gfile.GFile('R:/object_dection/facerecord/frozen_inference_graph.pb', 'rb') as fid:
      #with tf.gfile.GFile('R:/object_dection/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb', 'rb') as fid:
      with tf.gfile.GFile('R:/object_dection/facerecord/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb', 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap('R:/object_dection/facerecord/pascal_label_map.pbtxt')
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    cap = cv2.VideoCapture(0)

    width = 800
    height = 600

    cap.set(4, width);
    cap.set(3, height);

    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
        while True:
          ret, image_np = cap.read()

          print( image_np.shape )

          # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
          image_np_expanded = np.expand_dims(image_np, axis=0)
          image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
          # Each box represents a part of the image where a particular object was detected.
          boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
          # Each score represent how level of confidence for each of the objects.
          # Score is shown on the result image, together with the class label.
          scores = detection_graph.get_tensor_by_name('detection_scores:0')
          classes = detection_graph.get_tensor_by_name('detection_classes:0')
          num_detections = detection_graph.get_tensor_by_name('num_detections:0')

          (boxes, scores, classes, num_detections) = sess.run( [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
          vis_util.visualize_boxes_and_labels_on_image_array( image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32),
              np.squeeze(scores), category_index, use_normalized_coordinates=True, line_thickness=2)

          cv2.imshow('object detection', cv2.resize(image_np,(width,height)))

          if cv2.waitKey(25) & 0xFF ==ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
  tf.app.run()