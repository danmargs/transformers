from predictors import Predictor
from models import build_model
from datasets import IndexedInputTargetTranslationDataset
from dictionaries import IndexDictionary

from argparse import ArgumentParser
import json

parser = ArgumentParser(description='Predict translation')
parser.add_argument('--source', type=str)
parser.add_argument('--config', type=str, required=True)
parser.add_argument('--checkpoint', type=str)
parser.add_argument('--num_candidates', type=int, default=1)

args = parser.parse_args()
with open(args.config) as f:
    config = json.load(f)

print('Constructing dictionaries...')
source_dictionary = IndexDictionary.load(config['data_dir'], mode='source', vocabulary_size=config['vocabulary_size'])
target_dictionary = IndexDictionary.load(config['data_dir'], mode='target', vocabulary_size=config['vocabulary_size'])

print('Building model...')
model = build_model(config, source_dictionary.vocabulary_size, target_dictionary.vocabulary_size)

predictor = Predictor(
    preprocess=IndexedInputTargetTranslationDataset.preprocess(source_dictionary),
    postprocess=lambda x: ' '.join([token for token in target_dictionary.tokenify_indexes(x) if token != '<EndSent>']),
    model=model,
    checkpoint_filepath=args.checkpoint
)

f  = open("test/errori.txt", "a")
f.truncate(0)
f.close

f = open("test/errori.txt", "a")
f1 = open(args.source, "r") 
f2 = open("test/output.txt", "r") 
if f1.mode == 'r': 
    fl = f1.readlines()
    flo = f2.readlines()
    for i, frase in enumerate(fl, start=0):
        trovato = False
        for index, candidate in enumerate(predictor.predict_one(frase[:-1], num_candidates=args.num_candidates)):
            #print(frase[:-1] + " === " + flo[i][:-1] + " --> " +str(index) + " " + candidate )
            if (candidate == flo[i][:-1]):
                trovato = True
        if trovato == False :
            f.write(frase + frase + flo[i][:-1] + "\n" + flo[i][:-1] )
            f.write("\n \n")

f.close()
f1.close()
f2.close()


