from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer

def get_tokens(text):
        tokenized_sents = [word_tokenize(text) for i in text]
        for i in tokenized_sents:
            tokens = word_tokenize(text)
        return tokens

def do_stemming(filtered):
        stemmed = []
        for f in filtered:
            stemmed.append(LancasterStemmer().stem(f))
        return stemmed

if __name__ == "__main__":
        tex = "okay oka ok"
        tokens = get_tokens(tex)
        print("tokens = %s") %(tokens)
        stemmed_tokens = do_stemming(tokens)
        print("stemmed_tokens = %s") %stemmed_tokens
        #result = dict(zip(tokens, stemmed_tokens))
        #print("{tokens:stemmed} = %s") %(result)