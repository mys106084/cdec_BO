#import sys

train_url_en = 'corpus.en'
train_url_es = 'corpus.es'
train_out = 'corpus.es-en'

dev_url_en = 'dev.en'
dev_url_es = 'dev.es'
dev_out = 'dev.es-en'

def main():
	coutline = 0
	
	fin_es = open(train_url_es,'r')
	fin_en = open(train_url_en,'r')
	fout = open(train_out,'w')
	'''
	fin_es = open(dev_url_es,'r')
	fin_en = open(dev_url_en,'r')
	fout = open(dev_out,'w')
	'''

	while 1:
		line_en = fin_en.readline()
		if not line_en:
			break
		coutline += 1
		if coutline%1000 == 0:
			print 'Processing '+ str(coutline)
		line_es = fin_es.readline()
		fout.write(line_es[0:len(line_es)-1]+' ||| '+line_en)	# delelte the 'newline' charactor
	fin_es.close()
	fin_en.close()
	fout.close()

if __name__=='__main__':
  main()

