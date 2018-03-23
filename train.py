from histograms import Dictogram
import re
import argparse
import pickle
import os
import sys

r_alphabet = re.compile(u'[а-яa-zA-ZА-Я0-9-.,:;?!]+')


def new_parser1():  # Создание консольной оболочки
    pars = argparse.ArgumentParser(
        description='''Данная программа составляет последовательности из слов
         и сохраняет их в заданном файле.''',
        epilog='''(с) 2018. Created by Roslyakov Misha'''
    )
    pars.add_argument('--input', nargs='?',
                      help='Путь к тексту'
                           'Если данный аргумент не '
                           'задан, считается, что тексты вводятся из stdin или извлекаются из папки. '
                           'ВНИМАНИЕ: в конце ввода текстов из stdin '
                           'для завершения ввода '
                           'необходимо написать строку:"*END*" или пустую строку.')
    pars.add_argument('--input1', '--input-dir', nargs='?',
                      help='Путь к директории, в которой лежит коллекция '
                           'документов. Если данный аргумент не '
                           'задан, считается, что тексты вводятся из stdin. '
                           'ВНИМАНИЕ: в конце ввода текстов из stdin '
                           'для завершения ввода '
                           'необходимо написать строку:"*END*" или пустую строку.')
    pars.add_argument('--model', required=True,
                      help='Путь к файлу, в который сохраняется модель.'
                           'Формат файла *****.txt'
                           'хранить в папке с train.py и generate.py.')
    pars.add_argument('--lc', nargs='?', default=True,
                      help='Приводит текст к нижниму регистру')
    return pars


def gen_tokens(line_w):  # делим на слова
    for token in r_alphabet.findall(line_w):
        if lowercase is not True:
            yield token.lower()
        else:
            yield token


def make_markov_model(data):
    for i in range(0, len(data) - 1):
        if data[i] in models:
            # Просто присоединяем к уже существующему распределению
            models[data[i]].update([data[i + 1]])
        else:
            models[data[i]] = Dictogram([data[i + 1]])
    return models


models = dict()
parser1 = new_parser1()
commands = parser1.parse_args(sys.argv[1:])
way_to_file = commands.input1
name_file = commands.input
lowercase = commands.lc
if name_file is not None:
    with open(name_file, 'r', encoding='UTF-8') as file:
        for line in file:
            tokens = ['END']
            tokens += list(gen_tokens(line)) + ['ENDS']
            models = make_markov_model(tokens)
        file.close()
else:
    if way_to_file is not None:  # ищем путь к текстам
        d_list = os.listdir(way_to_file)
        txt_files = list(filter(lambda x: x.endswith('.txt'), d_list))
        for bad_file in txt_files:
            path = os.path.join(way_to_file, bad_file)
            with open(path, 'r', encoding='UTF-8') as file:
                for line in file:
                    tokens = ['END']
                    tokens += list(gen_tokens(line)) + ['ENDS']
                    print(len(tokens))
                    models = make_markov_model(tokens)
                    print(models)
                file.close()
    else:
        ls = ' '
        while ls != '*END*':
            try:
                ls = input().lower()
            except EOFError:
                break
            tokens = ['END']
            tokens += list(gen_tokens(ls)) + ['ENDS']
            models = make_markov_model(tokens)
with open(commands.model, 'wb') as f:
    pickle.dump(models, f)
