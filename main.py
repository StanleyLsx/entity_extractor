# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : main.py
# @Software: VScode
from loguru import logger
from config import use_cuda, cuda_device, configure, mode
from engines.data import DataManager
from engines.utils.setup_seed import setup_seed
from pprint import pprint
import torch
import os
import json


def fold_check(configures):
    if configures['checkpoints_dir'] == '':
        raise Exception('checkpoints_dir did not set...')

    if not os.path.exists(configures['checkpoints_dir']):
        print('checkpoints fold not found, creating...')
        os.makedirs(configures['checkpoints_dir'])


if __name__ == '__main__':
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    setup_seed(configure['seed'])
    fold_check(configure)
    log_name = './logs/' + mode + '.log'
    logger.add(log_name, encoding='utf-8')

    if use_cuda:
        if torch.cuda.is_available():
            if cuda_device == -1:
                device = torch.device('cuda')
            else:
                device = torch.device(f'cuda:{cuda_device}')
        else:
            raise ValueError(
                "'use_cuda' set to True when cuda is unavailable."
                " Make sure CUDA is available or set use_cuda=False."
            )
    else:
        device = 'cpu'
    logger.info(f'device: {device}')
    data_manager = DataManager(configure, logger=logger)

    if mode == 'train':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        from engines.train import Train
        logger.info('mode: train')
        Train(configure, data_manager, device, logger).train()
    elif mode == 'interactive_predict':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: predict_one')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.predict_one('warm up')
        while True:
            logger.info('please input a sentence (enter [exit] to exit.)')
            sentence = input()
            if sentence == 'exit':
                break
            logger.info('input:{}'.format(str(sentence)))
            result = predictor.predict_one(sentence)
            logger.info('putput:{}'.format(str(result)))
            pprint(result)
    elif mode == 'test':
        from engines.predict import Predictor
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: test')
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.predict_test()
    elif mode == 'convert_onnx':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: convert_onnx')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.convert_onnx()
    elif mode == 'show_model_info':
        logger.info(json.dumps(configure, indent=2, ensure_ascii=False))
        logger.info('mode: show_model_info')
        from engines.predict import Predictor
        predictor = Predictor(configure, data_manager, device, logger)
        predictor.show_model_info()
