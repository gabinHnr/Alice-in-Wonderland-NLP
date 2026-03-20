import csv
import argparse
import requests
import torch
import nltk
from transformers import T5Tokenizer, T5ForConditionalGeneration
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from heapq import nlargest


# on import nos modules python qui vont nous servir a plein de chose, ( fais a la main c'est juste pour avoir un code plus propre)
from Modules.Tokenization import tokenize_data
from Modules.Normalize import run_normalize
from Modules.Download_Book import download_book

# fonction d'initialisation qui permet d'initialiser tout ce qu'on na besoin pour le code
# def init():
parser = argparse.ArgumentParser()

def Info_Book():
    reader = csv.DictReader(open('pg_catalog.csv'))
    result = {}
    for row in reader:
        key = row.pop('Text#')
        if key in result:
            pass
        result[key] = {}
        Mydico = result[key]
        # on va aller chercher pour chaque ID, le titre, l'author, le bookshelves et l'id
        Mydico.update({'id': key, 'title': row['Title'], 'authors': row['Authors'], 'bookshelves': row['Bookshelves']})
    return result


Livre_infos = Info_Book()

download_book(Livre_infos, 11)



# fonction qui nous permnet d'avoir notre dictionnaire demande pour le lexdiv
def lexdiv():
    Dict_lexdiv = {}
    txt = tokenize_data("The little yellow duck !")
    print(run_normalize(txt))


def topic():
    book_id = args.topics[0]

    info = download_book(Livre_infos, book_id)
    sentences = sent_tokenize(info)
    sections = info.split("CHAPTER")
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    words = []
    for k in sentences:
        for j in nltk.word_tokenize(k):
            if j not in stop_words and j.isalpha():
                words.append(stemmer.stem(j))
    frequence = nltk.FreqDist(words)
    dixplusfrequent = [mots[0] for mots in frequence.most_common(10)]
    print (dixplusfrequent)
    # resume = []
    # for k in sentences:
    #     motsphrase = nltk.word_tokenize(k.lower())
    #     score = 0
    #     for j in k:
    #         if stemmer.stem(j) in dixplusfrequent:
    #             score += 1
    #     resume.append((k, score))
    # for k in nlargest(3, resume, key=lambda x: x[1]):
    #     print(k[0])


def summarize():
    book_id = args.summarize[0]

    info = download_book(Livre_infos, book_id)

    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    device = torch.device("cpu")

    preprocessed_text = info.strip().replace('\n', "")
    input_text = 'summarize: ' + preprocessed_text

    tokenized_text = tokenizer.encode(input_text, return_tensors='pt', max_length=1000, truncation=True).to(device)

    summary_id = model.generate(tokenized_text, min_length=30, max_length=120, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_id[0], skip_special_tokens = True)

    return(summary)

if args.topics:
    print(topic())


if args.lexdiv:
    print(lexdiv())

if args.summarize:
    print(summarize())