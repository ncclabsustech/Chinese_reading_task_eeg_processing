import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def generate_unique_array(length, upper_limit):
    """
    Generate a random vector with non-repeating elements. It is used to determine which positions in the data are masked
    :param length: The length of the vector that needs to be generated
    :param upper_limit: The upper bound of the elements in the vector
    :return: A random vector with non-repeating elements
    """
    if length > upper_limit:
        raise ValueError("Length cannot be greater than the upper limit.")

    unique_elements = np.arange(0, upper_limit)
    np.random.shuffle(unique_elements)
    unique_array = unique_elements[:length]
    return unique_array


def mask(eeg, mask_rate, same_place=False):
    """
    randomly mask eeg data
    :param eeg: numpy array，[n_channel, length]
    :param mask_rate: mask ratio，between [0, 1]
    :param same_place: Whether the mask positions are the same for each channel, the default is False
    :return: masked eeg data，numpy array，[n_channel, length]
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
    input_eeg = np.load(r"../data/random_mask/test.npy")[:, :1000] # (15, 2560)
    input_eeg_copy = np.copy(input_eeg)

    masked = mask(input_eeg_copy, mask_rate=0.75, same_place=False)
    plt.scatter(range(masked.shape[1]), masked[0], s=1, label="masked signal 0", c="green")
    plt.scatter(range(masked.shape[1]), masked[1], s=1, label="masked signal 1", c="red")
    plt.legend()
    plt.title("mask_rate=0.75, same_place=False")
    plt.show()





if __name__ == "__main__":
    main()

