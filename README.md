# GestureRecognitionPSIML6

This repo hosts individual assignment code for gesture recognition created (more-less) during Petnica Summer Institute of Machine Learning 6 [31.7.2020. - 10.8.2020.]
---

# RNN

That "more-less" part concerns the fact that I wasn't able to finish my RNN assignment in time for the duration of the seminar, so I continued working afterwards in order to get at least the most basic model working. Excuse my noobness, I still have a lot to learn.

My work (not concerning the CNN model) is located in `rnn_gesture_recognition` folder and contains the `code` subfolder (with currently miserable RNN gesture recognition model, achieving ~10% accuracy on [KARD](https://data.mendeley.com/datasets/k28dtm7tr6/1) &mdash; but it *is* working) and `images` subfolder with snippets from some papers I've read *after* the seminar, in an effort to better understand the matter. These snippets are used in jupyter notebook `rnn_gesture_recog_ref_analysis.ipynb` which summarizes read papers concerning the usage of RNNs in gesture recognition.

I'm leaving this material here for future PSIML students that may need it, and, of course, to all those that want to start using RNNs for gesture recognition and have trouble starting.

PyTorch API is used throughout.

Here are some links to people and resources that have helped me a lot when writing this code:
- [Dataloaders for large files](https://medium.com/swlh/how-to-use-pytorch-dataloaders-to-work-with-enormously-large-text-files-bbd672e955a0)
- [Parallel Data Generation with PyTorch (Stanford)](https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel)
- [Building Efficient Custom Datasets](https://towardsdatascience.com/building-efficient-custom-datasets-in-pytorch-2563b946fd9f)
- [Streaming Dataset](https://medium.com/speechmatics/how-to-build-a-streaming-dataloader-with-pytorch-a66dd891d9dd)
- [Building RNNs is Fun](https://medium.com/dair-ai/building-rnns-is-fun-with-pytorch-and-google-colab-3903ea9a3a79)
- [NLP from Scratch (PyTorch Official)](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html)
- [Dive into Deep Learning Book](https://d2l.ai/)

I intend to keep using this repo and update it as my skills with gesture recognition (hopefully) advance.

Best of luck!

FlyingPlushie
29.8.2020.
---

# Necessary libraries
[xmltodict](https://pypi.org/project/xmltodict/)
