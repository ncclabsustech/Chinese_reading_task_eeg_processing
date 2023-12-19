# Random Mask for EEG Data

## Introduction

This script aims at implementing random mask for EEG data.

## Environment Requirement

`matplotlib >= 3.7.0`

`numpy >= 1.25.0`

## Example

We use an EEG data of shape (15, 2560), where 15 is the channel number and 2560 stands for the data length. The data can be found in `data/random_mask/test.npy`.

Here is the example of how to use this scripts：

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

The result is shown below：
![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/random_mask1.png)

if `same_place=True`, Then all the channels are masked in the same place：

```
masked = mask(input_eeg_copy, mask_rate=0.75, same_place=True)
plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
plt.scatter(range(masked.shape[1]), masked[1], s=1, label="masked signal 1", c="red")
plt.legend()
plt.title("mask_rate=0.75, same_place=True")
plt.show()
```

![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/random_mask2.png)

if `same_place=False`，Then all the channels are **not** masked in the same place：


![](https://github.com/ncclabsustech/Chinese_reading_task_eeg_processing/blob/main/image/random_mask3.png)





## Main Functions

`generate_unique_array(length, upper_limit)`：Produce a random vector with no duplicated element. Used to determine the sites for masking.

`mask(eeg, mask_rate, same_place=False)`：To mask EEG data randomly.

