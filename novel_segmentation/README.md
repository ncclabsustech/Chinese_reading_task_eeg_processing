# Chinese language corpus segmentation 

## Introduction

This README file aims to illustrate how to segment Chinese novel using our code.

## Environment

We use `xlsx` files to save our segmented novel. We use the package `openpyxl` to write the content to excel files. You can install this package with pip:

```
pip install openpyxl
```

## Code Explanation

You should run `cut_Chinese_novel.py` to process your `.txt` formated Chinese novel for sentence segmentation, obtaining the corresponding formatted `.xlsx` files. 

`cut_Chinese_novel.py` is used to process the novel into a suitable format for presentation in the Psychopy program. The novel content will be segmented into a series of units, each containing no more than 10 Chinese characters, and adjacent three units will be combined to form the content of each frame during the screen presentation. The same combination of adjacent units will be repeated multiple times to facilitate the subsequent highlighting display of each individual character. Additionally, you can specify to divide the novel from certain chapters into several parts and output them as separate files.

​                                                                                                                                                                                                                                                         The input for this script must be a Chinese novel content in `.txt` format. The format of the novel content should meet the following requirements:

1. **The beginning of the file should contain the preface section with a sign Ch0**. The preface will be used as a simulation before reading the formal chapters.
2. Each subsequent chapter should start with a sign **Ch + \<chapter number>**.

Below is an example:

```
Chinese_novel.txt
Ch0
This is the preface of the novel
Ch1
Chapter 1 of the novel
Ch2
Chapter 2 of the novel
...
...
...
```

In real experiments, considering issues like eye tracker battery life, we must perform battery replacement during the experiment. Due to technical constraints, we have to temporarily stop the experiment program during battery replacement. Therefore, we may divide a complete novel into multiple parts and present each part during each complete program run. For example, we may divide a novel with 30 chapters to 4 parts, and we will run the program several times to finish the entire novel content. 

In this script, you can specify the chapters you want to divide the novel by changing parameter `divide_num` , and the program will divide the chapters and output the  files containing these different parts.

The outputs have three different types of data files:

- The first type of file contains one specific file that contains the entire content of the novel. Its contents are divided according to each line as it is displayed. This file is named `segmented_Chinese_novel.xlsx`.  In this type of data, **we removed all lines that do not contain Chinese characters, namely those lines composed entirely of punctuation marks.** This is based on the following reason: During the actual display process, lines that contain only punctuation are not presented in the central line of the screen for the subjects to read. Therefore, in the analysis of related EEG data, these lines do not have corresponding data segments. 
- The second type of file contains the content of each trial (i.e., the specified chapter played during one session), also divided according to each line as displayed, and these files are named `segmented_Chinese_novel_run_xx.xlsx`, where xx is the specific number of the run. **we also removed all lines that do not contain Chinese characters for the same reason as before.**
-  The third type of file is a specialized file used for projecting the content on the screen. It directly corresponds to the second type of file, with each file in the third type being a transformation of the second type. The primary purpose of these files is to present content on the screen via the Psychopy program, hence we add “display” at the end of the file name in the second type to denote this distinction. The format is like `segmented_Chinese_novel_run_xx_display.xlsx` 

We provide a `.txt` file of the novel *The Little Prince* and the processed `.xlsx` files as an example. 

#### Parameters

| Parameter          | type | usage                                                        |
| ------------------ | ---- | ------------------------------------------------------------ |
| divide_nums        | str  | Breakpoints which you want to divide your novel (comma-separated). e.g. If you want to break the novel from chapter 8, 16, 24, you should pass the argument as --divide_nums=8,16,24 |
| Chinese_novel_path | str  | Path to your `.txt` Chinese novel content                    |
| save_path          | str  | Path to save the outputs                                     |

#### Running

You can run this code using the following command:

```
python cut_Chinese_novel.py --divide_nums=<chapter numbers of the cutting point> --Chinese_novel_path=<path to your .txt file of the novel> --save_path=<path to save the outputs>
```



