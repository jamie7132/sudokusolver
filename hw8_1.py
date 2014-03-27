import re

def chunks(l, n):
  "Yield successive n-sized chunks from l."
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

def load_string(pstring):
  "Returns a 2D array representing the puzzle."
  cells = [int(n) for n in re.findall(r'[0-9]', pstring.replace('.', '0'))]
  return list(chunks(cells, 9))