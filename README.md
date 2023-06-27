# Entity Extractor  
使用torch编写的可以使用crf、logits、span、global_pointer四种方法进行实体识别任务的框架，ChatGPT时代以前常用来打ner比赛的框架，可以魔改，推荐使用torch2，具体的环境见requirements.txt。  
整合了项目[
entity_extractor_by_pointer](https://github.com/StanleyLsx/entity_extractor_by_pointer)和项目[entity_extractor_by_ner](https://github.com/StanleyLsx/entity_extractor_by_ner)两个训练框架的大一统框架，通过对configure.py文件进行配置，运行main.py可以对模型进行训练、交互预测、跑测试集、转换onnx和打印模型的结构信息。     
训练过程中，框架会打印每一类的实体的指标。  
```
# 模式
# train:                训练分类器
# interactive_predict:  交互模式
# test:                 跑测试集
# convert_onnx:         将torch模型保存onnx文件
# show_model_info:      打印模型参数
mode = 'train'
```

仅支持单卡训练，请在configure.py文件中通过指定cuda_device控制使用某一张卡，或令use_cuda=False使用CPU进行训练。  
```
# 使用GPU设备
use_cuda = True
cuda_device = 0
```

## 更新历史
日期| 版本     |描述
:---|:-------|---
2022-12-01| v1.0.0 |初始仓库
2022-12-09| v1.1.0 |完成除蒸馏以外的所有逻辑
2023-01-09| v1.2.0 |增加直接从transformer读取模型，并支持英文的span方法训练

## 支持的数据输入格式
* BIO格式标注的文件  
具体的格式请参考data/example_datasets4目录下的csv文件
  
* json格式标注的文件  
具体的格式请参考data/example_datasets1目录下的csv文件

## 支持的tricks  
tricks| 细节
:---|-------
kfold交叉验证|支持
不使用预训练模型时候的字词粒度|可以选择
支持的ner任务|序列标注、span方式、global_pointer、传统的crf的各类组合，具体请看configure.py文件
损失函数|span方法可选苏神的多标签损失函数、BCELoss，crf默认使用对数似然损失、logints方法使用交叉熵损失
对抗方法|fgsm、fgm、pgd、awp
noisy_tune|支持
warmup|支持
随机权重平均swa|支持
ema|支持
early_stop|支持
multisample dropout|支持
