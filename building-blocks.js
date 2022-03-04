
const tf = require('@tensorflow/tfjs-node');
const a = [1,2,3,4,5,6]
const t1 = tf.tensor2d(a, [2,3], dtype = "float32");
t1.print();
