import sys, os
import numpy as np
import matplotlib.pyplot as plt

# optimizerのインポート
from AdaGrad.AdaGrad import AdaGrad
from Adam.Adam import Adam
from Momentum.Momentum import Momentum
from SGD.SGD import SGD

# 現在のファイル(optimizer_compare_mnist.py)があるディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# その親ディレクトリを取得
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)
# ネットワークのインポート
from network.multi_layer_net import MultiLayerNet

# データのインポート
from data.mnist import load_mnist

# 損失曲線を平滑化する関数をインポート
from utils.smooth import smooth_curve

# 0:MNISTデータの読み込み==========
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)

train_size = x_train.shape[0]
batch_size = 128
max_iterations = 2000


# 1:実験の設定==========
optimizers = {}
optimizers['SGD'] = SGD()
optimizers['Momentum'] = Momentum()
optimizers['AdaGrad'] = AdaGrad()
optimizers['Adam'] = Adam()

networks = {}
train_loss = {}
for key in optimizers.keys():
    networks[key] = MultiLayerNet(
        input_size=784,
        hidden_size_list=[100, 100, 100, 100],
        output_size=10
    )
    train_loss[key] = []   

# 2:訓練の開始==========
for i in range(max_iterations):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]
    
    for key in optimizers.keys():
        grads = networks[key].gradient(x_batch, t_batch)
        optimizers[key].update(networks[key].params, grads)
    
        loss = networks[key].loss(x_batch, t_batch)
        train_loss[key].append(loss)
    
    if i % 100 == 0:
        print( "===========" + "iteration:" + str(i) + "===========")
        for key in optimizers.keys():
            loss = networks[key].loss(x_batch, t_batch)
            print(key + ":" + str(loss))

# 3.グラフの描画==========
markers = {"SGD": "o", "Momentum": "x", "AdaGrad": "s", "Adam": "D"}
x = np.arange(max_iterations)
for key in optimizers.keys():
    plt.plot(x, smooth_curve(train_loss[key]), marker=markers[key], markevery=100, label=key)
plt.xlabel("iterations")
plt.ylabel("loss")
plt.ylim(0, 1)
plt.legend()
plt.show()
