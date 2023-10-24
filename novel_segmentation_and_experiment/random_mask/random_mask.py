import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def generate_unique_array(length, upper_limit):
    """
    产生一个随机的，每个元素不重复的向量。用于决定mask掉数据中哪些位点。
    :param length: 需要产生的向量的长度。
    :param upper_limit: 向量中元素的上界。
    :return: 一个随机的，每个元素不重复的向量
    """
    if length > upper_limit:
        raise ValueError("Length cannot be greater than the upper limit.")

    unique_elements = np.arange(0, upper_limit)
    np.random.shuffle(unique_elements)
    unique_array = unique_elements[:length]
    return unique_array


def mask(eeg, mask_rate, same_place=False):
    """
    随机mask eeg数据
    :param eeg: numpy数组，[n_channel, length]
    :param mask_rate: mask比例，在0到1之间
    :param same_place: 每个通道mask的位置是否一样，默认为False
    :return: mask后的eeg，numpy数组，[n_channel, length]
    """

    mask_length = round(eeg.shape[1] * mask_rate)


    if same_place:
        mask_places = generate_unique_array(mask_length, eeg.shape[1])
        for place in mask_places:
            eeg[:, place] = 0
    else:
        for channel in range(eeg.shape[0]):
            mask_places = generate_unique_array(mask_length, eeg.shape[1])
            for place in mask_places:
                eeg[channel:channel+1, place] = 0

    return eeg

def main():
    input_eeg = np.load("test.npy")[:, :1000] # (15, 2560)
    input_eeg_copy = np.copy(input_eeg)
    # masked = mask(input_eeg_copy, mask_rate=0.75, same_place=True)

    # plt.scatter(range(input_eeg.shape[1]), input_eeg[0], s=1, label="origin signal 0", c="red")
    # plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
    # plt.legend()
    # plt.title("mask_rate=0.75, same_place=True")
    # plt.show()

    masked = mask(input_eeg_copy, mask_rate=0.75, same_place=False)
    plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
    plt.scatter(range(masked.shape[1]), masked[1], s=1, label="masked signal 1", c="red")
    plt.legend()
    plt.title("mask_rate=0.75, same_place=False")
    plt.show()





if __name__ == "__main__":
    main()

