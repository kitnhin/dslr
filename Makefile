TRAIN_DATASET = datasets/dataset_train.csv
PREDICT_DATASET = datasets/dataset_test.csv

GRADIENT_DESCEND = minibatch #batch, minibatch, sgd

describe:
	@python3 describe.py ${TRAIN_DATASET}

hist:
	@python3 histogram.py ${TRAIN_DATASET}

scatter:
	@python3 scatter.py ${TRAIN_DATASET}

pair:
	@python3 pair_plot.py ${TRAIN_DATASET}

train:
	@python3 logreg_train.py --trainDataset ${TRAIN_DATASET} --gradientDescend ${GRADIENT_DESCEND}

predict:
	@python3 logreg_predict.py ${PREDICT_DATASET}

run: train predict acc

acc:
	@python3 evaluate.py

clean:
	rm houses.csv params.json

all: describe