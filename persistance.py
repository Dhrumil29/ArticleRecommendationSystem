import shelve

data = shelve.open("reverseIndex")

data.close()