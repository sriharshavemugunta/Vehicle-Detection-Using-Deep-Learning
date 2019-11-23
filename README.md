# Vehicle-Detection-Using-Deep-Learning

Introduction : Visual tracking has long been a fundamental research problem in computer vision. Although numerous algorithms have been proposed for moving objects, it remains a challenging problem to handle large appearance variations, abrupt motion, severe occlusions, and background clutters. Existing machine learning algorithms are dependent on hand-crafted features such as shape, color or texture for object classification and has overfitting problem. With the development of deep learning technology, Neural networks achieved promising accuracy better than humans for object detection and classification. In this project, we used Faster-RCNN algorithm for detecting cars in satellite images. Faster-RCNN is not as fast as other Neural networks because it has two layered architecture, but gives better accuracy than other neural networks. We used Cars Overhead with Context (COWC) dataset which contains contextual matter to aid in identiﬁcation of difficult targets. 

Methodology : 
1. Initialization –  Initialize the patch size, step size and car size as 256, 128 and 32 respectively. 
2. Image Acquisition -  Load the pickle file into item list. In the first iteration, process the first directory in item list by reading raw image files.
3. Pre-processing – Convert each raw image file into matrix notation. Divide the matrix into steps.
     steps_x = raw_image.shape[1] / step_size
     steps_y = raw_image.shape[0] / step_size
4. Vehicle Detection - Extract the object locations in the matrix and determine the step location of each object. Remove patches whose shape exceeds the shape of matrix. Read the image patch and write locations and dimensions of a car into text file.
5. Bounding Boxes – Based on the locations, draw a bounding box around car.

DataSet : 
Data from overhead at 15 cm per pixel resolution at ground.
Data from six distinct locations: Toronto - Canada, Selwyn - New Zealand, Potsdam and Vaihingen - Germany, Columbus and Utah – United States. 
32,716 unique annotated cars. 58,247 unique negative examples.

Summary of Drawbacks : 
1. Bounding boxes were ﬁxed at size x*x pixels which is the maximum length of a car if we use ResCeption network.
2. It is a challenging task, due to the complex background, diverse colors and occlusions caused by buildings and trees. 
3. Only detect vehicles on road if we use Deep Convolutional Neural Network (DNN).
