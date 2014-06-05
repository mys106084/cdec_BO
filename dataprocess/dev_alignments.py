import sys
def main(cdec_out,fscore_out):
	fin = open(cdec_out,'r')
	fout = open(fscore_out,'w')
	coutline = 0
	while 1:
		line = fin.readline()
		if not line:
			break
		output = line.split('|||')
		if len(output) >3:
			coutline += 1
			alignments = output[2].split(' ')
			for i in xrange(0,len(alignments)):
				es_en = alignments[i].split('-')
				if len(es_en)==2:
					fout.write(str(coutline)+' '+str(int(es_en[1])+1) +' '+str(int(es_en[0])+1) +'\n') 
	fin.close()
	fout.close()
	#print 'Finish transformation!'

if __name__=='__main__':
	if len(sys.argv) != 3:
		print 'Wrong Parameters'
		sys.exit(1)
	main(sys.argv[1],sys.argv[2])