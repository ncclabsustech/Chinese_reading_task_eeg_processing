# split_text

## 功能概述

本代码旨在实现中/英文文本的分割。

## 依赖项

import jieba >= 0.42.1

import numpy >= 1.23.5

## 测试数据

《小王子》中文译本

## 使用示例

以下是如何使用该代码的示例。以《小王子》中文译本为例：

```
import re
import jieba
import numpy as np

def main():
    filename = "test.txt"

    result = split(filename, language="Chinese")

    for e in result:
        print(e)
```

输入文本：我把这幅杰作给大人看，问他们我的图画吓不吓人。他们回答说：“一顶帽子怎么会吓人呢？”

运行代码结果如下：

[[[{'text': '我把这幅杰作给大人看，', 'index': array([1., 1., 0., 1., 0., 1., 1., 0., 1., 1., 1.])}, {'text': '问他们我的图画吓不吓人。', 'index': array([1., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1.])}], [{'text': '他们回答说：', 'index': array([0., 1., 0., 1., 1., 1.])}]]
[[{'text': '“一顶帽子怎么会吓人呢？”', 'index': array([1., 0., 1., 0., 1., 0., 1., 1., 0., 1., 1., 1., 1.])}]]]

第一层列表：偶数index的元素为非引号内的文本，奇数index内的元素为引号内的文本。所有元素均为列表。

第二层列表：每个文本按句末符号（问号、感叹号、句号）切分后的文本。所有元素均为列表。

第三层列表：每个文本按逗号切分后的文本，所有元素均为字典。

字典：包含两个field，“text”为原文本，“index”为原文本经过分词后得到的index，每个字符的index为0或1。若为1，该字符位于词尾，0则为非词尾。例子：'text': '蟒蛇把猎物囫囵吞下，', 对应的分词结果为'蟒蛇|把|猎物|囫囵|吞|下|，|' 对应的'index': array([0., 1., 1., 0., 1., 0., 1., 0., 1., 1.])}

## 主要函数

`to_sentences(paragraph, mode, language)`: 对给定文本进行按标点切分

`str2dict(text, language)`: 将文本string进行切词，返回一个字典

`split(file_path, language)`: 面向用户的函数，主要用来调用to_sentences
