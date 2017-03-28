#!/bin/zsh
python ../deep_learning/examples/retrain_cnn_example.py  -d "../dataset" -s "../output/train_simple" -t "simple"
python ../deep_learning/examples/retrain_cnn_example.py  -d "../dataset" -s "../output/train_lenet" -t "lenet"