import numpy as np

class Sigmoid:
    """
    Sigmoidレイヤ : このレイヤは、シグモイド関数を使用して入力値を変換する。
    """
    def __init__(self):
        """
        Sigmoidレイヤの初期化メソッド。
        """
        self.out = None # 順伝播で使用する出力を初期化
    
    def forward(self, x):
        """
        順伝播（forward propagation） : 入力された値（x）に対してシグモイド関数を適用し、その結果を返す。

        Parameters
        ----------
        - x : 入力値（NumPy配列）

        Returns
        -------
        - out : シグモイド関数を適用した出力値
        """
        out = 1 / (1 + np.exp(-x))
        self.out = out

        return out # 出力値を返す
    
    def backward(self, dout):
        """
        逆伝播（backward propagation） : 順伝播で計算した出力を使用して、勾配（dout）を計算する。

        Parameters
        ----------
        - dout : 勾配（NumPy配列）

        Returns
        -------
        - dx : シグモイド関数の勾配
        """
        dx = dout * (1.0 - self.out) * self.out

        return dx # 勾配を返す