
import os


import tensorflow as tf, sys
# surpress warning logg
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# change this as you see fit
image_path = sys.argv[1]
#image_path="/tf_files/classifying_image.jpg"

# Read in the image_data
image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("/tf_files/fox_retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/tf_files/fox_retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    # print as json
    print("{")
    for node_id in top_k[:-1]:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        print('"%s":"%.5f",' % (human_string, score))
    # last one without semiconlon
    node_id = top_k[-1]
    human_string = label_lines[node_id]
    score = predictions[0][node_id]
    print('"%s":"%.5f"' % (human_string, score))

    print ("}")
