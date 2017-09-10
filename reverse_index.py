

class ReverseIndex(object):

    def __init__(self,text):
        self.text = text.split()
        #print self.text
        self.index = dict()
        #print self.index
    def generate_index(self,mutator=lambda x:x):
        self._generate_index(mutator)

    def _generate_index(self,mutator):
        for word in self.text:
            self.index[mutator(word)]= self.index.get(mutator(word),0)+1
    def find_index(self,word):
        return self.index.get(word,0)




