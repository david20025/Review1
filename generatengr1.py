from histograms import Dictogram
import argparse
import sys
import random
import os
import pickle
import math


def new_parser():  # Создаем консольную оболочку
    pars = argparse.ArgumentParser(
        description='''Эта программа принимает на вход словарь,
        составленный с помощью программы train.py, и на его основе
        генерирует свой текст. Надо ввести путь к файлу
        со словарем и длину выводимой последовательности.''',
        epilog='''(с) 2018. Created by Roslyakov Misha'''
    )
    pars.add_argument('--seed', nargs='?', default='**END**',
                      help='Задает начальное слово. Если не указано, '
                           'выбираем слово случайно из всех слов '
                           '(не учитывая частоты).')
    pars.add_argument('--length', type=int, required=True,
                      help='Длина генерируемой последовательности.')
    pars.add_argument('--model', required=True,
                      help='Путь к файлу, из которого загружается модель.'
                           'Вид файла *****.text'
                           'и находиться в папке с файлами программы.')
    pars.add_argument('--output', nargs='?',
                      help='Файл, в который будет записан результат. '
                           'Если аргумент отсутствует, выводить в stdout.')
    pars.add_argument('--n', required=True, help='по какой глубине строить')
    return pars


def generate_random_start(model):  # создаем рандомное начало
    for j in model.keys():
        if '**END**' in j:
            seed = j
            while seed == '**END**':
                seed = model[j].return_weighted_random_word()
            return seed
        return random.choice(list(model.keys()))


def generate_random_sentence(length, markov_model):  # создаем предложение заданной длины
    searched = 0
    for j in markov_model.keys():
        if seed_w != '**END**':
            if seed_w in j:
                searched = 1
                current_word = j
                break
        else:
            current_word = generate_random_start(markov_model)
            break
    if searched == 0:
        current_word = generate_random_start(markov_model)
    sentence = []
    i = 0
    for l in range(n):
        if current_word[l] != '**ENDS**':
            sentence.append(current_word[l])
            i += 1
        if i == length:
            sentence[0] = sentence[0].capitalize()
            return ' '.join(sentence) + '.'
            return sentence
    current_word = markov_model[current_word].return_weighted_random_word()
    while i < length:
        while '**ENDS**'==current_word:
            current_word = generate_random_start(markov_model)
            current_word = current_word[0]
        lis=list(markov_model.keys())
        random.shuffle(lis)
        flag = 1
        for j in lis:
            if current_word == j[0]:
                flag = 0
                tupt = tuple(j)
                current_dictograms = markov_model[tupt]
                random_weighted_word = current_dictograms.return_weighted_random_word()
                current_word = random_weighted_word
                while current_word == '**ENDS**':
                    current_word = generate_random_start(markov_model)
                    current_word = current_word[0]
                else:
                    for k in range(n):
                        sentence.append(tupt[k])
                        i += 1
                        if i == length:
                            break
                break
        if flag == 1:
            current_word = generate_random_start(markov_model)
            current_word = current_word[0]
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'
    return sentence


parser = new_parser()
commands = parser.parse_args(sys.argv[1:])
model_file = commands.model
seed_w = commands.seed
n = int(commands.n)
with open(model_file, 'rb') as file:
    models = pickle.load(file)
len_s = commands.length
phrase = generate_random_sentence(int(len_s), models)
if not commands.output:
    print('Our text:')
    print(phrase)
else:
    out_file = open(commands.output, 'w')
    out_file.write(phrase)
