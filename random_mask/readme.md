# random_mask

## 功能概述

本代码旨在实现EEG数据的随机掩码。

## 依赖项

import matplotlib >= 3.7.0

import numpy >= 1.25.0

## 测试数据

test.npy，一段(15, 2560)的EEG数据。15为通道数，2560为长度。

## 使用示例

以下是如何使用该代码的示例：

```
import numpy as np
import matplotlib.pyplot as plt

input_eeg = np.load("test.npy")[:, :1000] # (15, 2560)
input_eeg_copy = np.copy(input_eeg)
masked = mask(input_eeg_copy, mask_rate=0.75, same_place=True)

plt.scatter(range(input_eeg.shape[1]), input_eeg[0], s=1, label="origin signal 0", c="red")
plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
plt.legend()
plt.title("mask_rate=0.75, same_place=True")
plt.show()
```

运行代码结果如下：
![](https://files.mdnice.com/user/42793/899ef05f-c530-4870-8afe-3ec0f9e2a557.png)

若`same_place=True`，则所有通道mask的位点一致：

```
masked = mask(input_eeg_copy, mask_rate=0.75, same_place=True)
plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
plt.scatter(range(masked.shape[1]), masked[1], s=1, label="masked signal 1", c="red")
plt.legend()
plt.title("mask_rate=0.75, same_place=True")
plt.show()
```

![](https://files.mdnice.com/user/42793/0a875d8e-7e01-403f-8a07-2ac04fe422d0.png)

若`same_place=False`，则所有通道mask的位点不一致：


![](https://files.mdnice.com/user/42793/cc97c6a7-542f-4280-8aa1-00544ecf2e45.png)





## 主要函数

`generate_unique_array(length, upper_limit)`：产生一个随机的，每个元素不重复的向量。用于决定mask掉数据中哪些位点。

`mask(eeg, mask_rate, same_place=False)`：随机mask EEG数据。


