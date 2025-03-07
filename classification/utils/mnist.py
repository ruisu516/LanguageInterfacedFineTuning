import numpy as np
from urllib import request
import gzip
import pickle
import pandas as pd

filename = [
["training_images","train-images-idx3-ubyte.gz"],
["test_images","t10k-images-idx3-ubyte.gz"],
["training_labels","train-labels-idx1-ubyte.gz"],
["test_labels","t10k-labels-idx1-ubyte.gz"]
]

def download_mnist():
    base_url = "http://yann.lecun.com/exdb/mnist/"
    for name in filename:
        print("Downloading "+name[1]+"...")
        request.urlretrieve(base_url+name[1], name[1])
    print("Download complete.")

def save_mnist():
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1,28*28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    with open("mnist.pkl", 'wb') as f:
        pickle.dump(mnist,f)
    print("Save complete.")

def init():
    download_mnist()
    save_mnist()

def load(name='mnist'):
    if name == 'mnist':
        with open("utils/mnist.pkl",'rb') as f:
            mnist = pickle.load(f)
        return mnist["training_images"], mnist["training_labels"], mnist["test_images"], mnist["test_labels"]
    elif name == 'fmnist':
        X , y = {}, {}
        for mode in ['train', 'test']:
            data = pd.read_csv(f"data/fmnist_{mode}.csv")
            y[mode]= data["label"].values
            X[mode] = data.drop(["label"], axis=1).values

        return X['train'], y['train'], X['test'], y['test']
    elif name == 'cifar10':
        from keras.datasets import cifar10
        (X_train, y_train), (X_test, y_test) = cifar10.load_data()
        return X_train, y_train, X_test, y_test
        

if __name__ == '__main__':
    init()


