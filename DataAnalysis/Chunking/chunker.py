from nltk.chunk import ne_chunk
from nltk.corpus import treebank_chunk
from DataCleaning.POSTagger import tagger

sentence = "NLTK comes with a pre-trained named entity chunker. This chunker has been trained on data from the ACE program, National Institute of Standards and Technology (NIST) sponsored program for Automatic Content Extraction, which you can read more about"
tagged_sentence = tagger.tag(sentence.split())
print(tagged_sentence)
print(ne_chunk(tagged_sentence))

print(treebank_chunk.tagged_sents()[0])
print(ne_chunk(treebank_chunk.tagged_sents()[0]))