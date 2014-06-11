from time import time
from bo import BO
import numpy as np
import os
import sys
import subprocess

path_cdec = '/home/brian/workspace/cdec'

#(1) training, dev, test data #Put in cdec/python
path_training = 'training.es-en'
path_dev = 'dev.es-en'
path_test = 'test.es-en'
#(2) cdec.ini  #Put in cdec/python
#path_cdecinit = 'cdec.ini'
#(3) #Edit cdec/python/cdec.ini

# S.1 fastAlignment
#path_aligner = path_cdec + '/word-aligner/fast_align'
#path_aligner =  '../word-aligner/fast_align'
path_fa_output = 'training.es-en.fwd_align'

# S.2 extractor
#path_extractinit =  'extract.ini'
path_train_sa = path_cdec + 'tranin.sa'

# S.3 grammar
path_devsgm = path_cdec + 'dev.es-en.sgm'
path_testsgm = path_cdec + 'test.es-en.sgm'
path_devgrammar = path_cdec + 'dev.grammars'
path_testgrammar = path_cdec + 'test.grammars'

# for CdecFastAlignmentObjective
'''
path_BO = '/home/brian/workspace/cdec_BO'
path_aligner = path_cdec + '/word-aligner/fast_align'
path_transformer = path_BO + '/dataprocess/dev_alignments.py'
path_evaluater = path_BO + '/f-score/eval_alignment.py'

path_trainingdata = path_BO+'/dataprocess/training.es-en'
path_devdata= path_BO+'/dataprocess/dev.es-en'
path_fa_output = path_BO+'/dataprocess/test.out'
path_devout = path_BO+'/dataprocess/dev.out'
path_key = path_BO+'/f-score/dev.key'
'''
# for CdecAlignmentBLEUObjective
'''
path_trainingdata = path_cdec+'/BO_BLEU/training.es-en'
path_devdata = path_cdec+'/BO_BLEU/dev.lc-tok.es-en'
path_devtestdata = path_cdec+'/BO_BLEU/devtest.lc-tok.es-en'

path_fa_output = path_cdec+'/BO_BLEU/training.es-en.fwd_align'
path_aligner = path_cdec + '/word-aligner/fast_align'

path_extractinit =  path_cdec + '/BO_BLEU/extract.ini' 
path_cdecinit = path_cdec + '/BO_BLEU/cdec.ini' 
path_sa = path_cdec + '/BO_BLEU/tranin.sa'
path_devsgm = path_cdec + '/BO_BLEU/dev.lc-tok.es-en.sgm'
path_devtestsgm = path_cdec + '/BO_BLEU/devtest.lc-tok.es-en.sgm'
path_devtestsgm_cut = 'devtest.lc-tok.es-en.sgm'
path_devgrammar = path_cdec + '/BO_BLEU/dev.grammars'
path_devtestgrammar = path_cdec + '/BO_BLEU/devtest.grammars'
'''
class IBM2Objective(object):
    def __init__(self):
        self.domain = np.transpose(np.array([[0.01, 0.2],[0.0001,0.002],[0.01,0.2]]))
        self.ndim = 3
        
    def map_params(self, x):
        params = x.ravel()
        return params
    
    def __call__(self, x):
        
        params = self.map_params(x)
        return runIBM2(params)
        
        
        
class FastAlignmentObjective(object):
    def __init__(self):
        self.domain = np.transpose(np.array([[0.01, 0.2],[0.0001,0.002],[0.1,20]]))
        self.ndim = 3
        
    def map_params(self, x):
        params = x.ravel()
        return params
    
    def __call__(self, x):
        
        params = self.map_params(x)
        return runfastAlignment(params)


class CdecObjective(object):
    def __init__(self):
        self.domain = np.transpose(np.array([[0.01, 0.2],[0.0001,0.002],[0.1,20]]))
        self.ndim = 3
        
    def map_params(self, x):
        params = x.ravel()
        return params
    
    def __call__(self, x):   
        params = self.map_params(x)
        print str(params[0])+ ' ' +str(params[1]) + ' ' +str(params[2])
        
        
        pipe_in,pipe_out,pipe_err= os.popen3(path_aligner + ' -i ' +path_trainingdata + ' -x ' + path_devdata + ' -d -v -H -x ' +
                      ' -prob_align_null '+str(params[0]) +' -a '+str(params[1]) + ' -T ' + str(params[2]) , 'wr' )
        '''
        
        p = subprocess.Popen('/home/brian/workspace/cdec/word-aligner/fast_align -i /home/brian/workspace/cdec/training.es-en -d -v -o -H -x /home/brian/workspace/cdec/test.es-en'+
                      ' -prob_align_null '+str(params[0]) +' -a '+str(params[1]) ,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (pipe_in,pipe_out,pipe_err)=(p.stdin, p.stdout, p.stderr)
        '''
        line = ''
        elements = []
        while 1:
            line = pipe_err.readline()
            if '' == line:
                break
            elements = line.split()
            #print "BO INFO: "+ line
        # TOTAL LOG PROB -18901.8
        
        
        score = 0
        if elements[len(elements)-1]=='-inf':
            score = -9999999
        else:
            score = float(elements[len(elements)-1])
                
        print 'Result Likelihood:'+str(score)
        
        #score -1000
        return score
    
class CdecFastAlignmentObjective(object):
    def __init__(self):
        self.domain = np.transpose(np.array([[0.01, 0.2],[0.0001,0.002],[0.1,20]]))
        self.ndim = 3
        
    def map_params(self, x):
        params = x.ravel()
        return params
    
    def __call__(self, x):   
        params = self.map_params(x)
        print str(params[0])+ ' ' +str(params[1]) + ' ' +str(params[2])
        
        cmd = path_aligner + ' -i ' + path_trainingdata + ' -x ' + path_devdata+ ' -d -v  '+' -prob_align_null '+str(params[0]) +' -a '+str(params[1]) + ' -T ' + str(params[2]) 
        #print cmd
        #+ ' > /home/brian/workspace/cdec_BO/dataprocess/test.out'

        pipe_in,pipe_out,pipe_err= os.popen3(cmd, 'wr' )

        fout = open(path_fa_output,'w')
        line = ''
        while 1:
            line = pipe_out.readline()
            if '' == line:
                break
            fout.write(line)
        fout.close()
        print '1. Finish Alignment! \n'

        
        pipe_in,pipe_out,pipe_err= os.popen3('python '+ path_transformer +' '+  path_fa_output +' '+  path_devout,'wr')
        line = ''
        while 1:
            line = pipe_out.readline()
            if '' == line:
                break
            print line
        print '2. Finish Transform! \n'

        pipe_in,pipe_out,pipe_err= os.popen3('python ' + path_evaluater +' '+ path_key +' '+  path_devout,'wr')

        print '3. Finish Evaluation! \n'
        
        line = ''
        elements = []
        while 1:
            line = pipe_out.readline()
            if '' == line:
                break
            elements = line.split()
            #print "BO INFO: "+ line
        # TOTAL LOG PROB -18901.8
        
        
        score = 0
        
        if elements[len(elements)-1]=='-inf':
            score = -9999999
        else:
            score = float(elements[len(elements)-1])
                
        print 'Result f-score:'+str(score)
        
        #score -1000
        return score

class CdecAlignmentBLEUObjective(object):
    def __init__(self):
        self.domain = np.transpose(np.array([[0.01, 0.2],[0.0001,0.002],[0.1,20]]))
        self.ndim = 3
        
    def map_params(self, x):
        params = x.ravel()
        return params
    
    def __call__(self, x):   
        params = self.map_params(x)
        print str(params[0])+ ' ' +str(params[1]) + ' ' +str(params[2])

        # 0. Preprocess: (1) filter (2) Language model (3) .ini 

        # Set the current working directory
        os.chdir(path_cdec+'/python')

        # 1. word alignment
        cmd1 = path_aligner + ' -i ' + path_trainingdata + ' -d -v  '+' -prob_align_null '+str(params[0]) +' -a '+str(params[1]) + ' -T ' + str(params[2]) 
        p = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True, close_fds=True)
        (pipe_in, pipe_out) = (p.stdin, p.stdout)
        fout = open(path_fa_output,'w')
        line = ''
        while 1:
            line = pipe_out.readline()
            if '' == line:
                break
            fout.write(line)
        fout.close()
        print '1. Finish Alignment! \n'

        
        # 2. Compile training data (suffix array)
        cmd2 = 'python ' + path_cdec + '/python/cdec/sa/compile.py' + ' -b '+ path_training + ' -a ' +  path_fa_output + ' -c ' + 'extract.ini' + ' -o ' + path_train_sa
        print cmd2
        p = subprocess.Popen(cmd2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True,env = {'PYTHONPATH': path_cdec+'/python'})
        (pipe_in, pipe_out, pipe_err) = (p.stdin, p.stdout, p.stderr)
        while 1:
            line = pipe_err.readline()
            if '' == line:
                break
            print line
        print '2. Finish Compiling! \n'
        
        # 3. Extract grammar
        cmd3 = 'python ' + path_cdec + '/python/cdec/sa/extract.py ' +  ' -c '+ 'extract.ini' + ' -g ' + path_devgrammar+ ' -j 2 -z ' + ' < ' + path_dev +' > '+ path_devsgm
        print cmd3 
        p = subprocess.Popen(cmd3, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True,env = {'PYTHONPATH': path_cdec+'/python'})
        (pipe_in, pipe_out, pipe_err) = (p.stdin, p.stdout, p.stderr)
        while 1:
            line = pipe_err.readline()
            if '' == line:
                break
            print line
        
        cmd3 = 'python ' + path_cdec + '/python/cdec/sa/extract.py ' +  ' -c '+ 'extract.ini' + ' -g ' + path_testgrammar+ ' -j 2 -z ' + ' < ' + path_test +' > '+ path_testsgm
        p = subprocess.Popen(cmd3, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True,env = {'PYTHONPATH': path_cdec+'/python'})
        (pipe_in, pipe_out, pipe_err) = (p.stdin, p.stdout, p.stderr)
        while 1:
            line = pipe_err.readline()
            if '' == line:
                break
            print line
            elements = line.split()


        print '3. Finish Grammar Extraction! \n'
        
        # 4. Mira  
        # Mira make a fixed reference of path_devtestsgm_cut, so we can not use the full url link here
        
        cmd4 = 'python ' + path_cdec + '/training/mira/mira.py ' +  ' -d '+ path_devsgm + ' -t ' + path_testsgm+ ' -c ' + 'cdec.ini' + ' -j 2'
        print cmd4
        p = subprocess.Popen(cmd4, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True,env = {'PYTHONPATH': path_cdec+'/python'})
        (pipe_in, pipe_out, pipe_err) = (p.stdin, p.stdout, p.stderr)
        
        score = 0
        results = ['','','','','','','']
        i = 0
        while 1:
            results[i%7] = pipe_err.readline()
            if '' == results[i%7]:
                break
            print results[i%7]
            i += 1
        print results
        for j in xrange(0,7):
            elements = results[j].strip().split('=')
            if len(elements)>1:
                print elements
                if elements[0]=='BLEU':
                    print 'The score is:'+ elements[1]
                    score = float(elements[1])
        print '4. Finish Translation! \n'
        return score

if __name__ == '__main__':
    
    # IBM2
    '''
    x0 = np.random.randint(1,20,(20,1))*1.0/1000 
    x1 = np.random.randint(1,20,(20,1))*1.0/10000
    x2 = np.random.randint(1,20,(20,1))*1.0/100
    
    # fastAlignment
    x0 = np.random.randint(1,20,(200,1))*1.0/1000 
    x1 = np.random.randint(1,20,(200,1))*1.0/10000
    x2 = np.random.randint(1,200,(200,1))*1.0/10
    '''
    #cdec
    x0 = np.random.randint(1,20,(200,1))*1.0/1000 
    x1 = np.random.randint(1,20,(200,1))*1.0/10000
    x2 = np.random.randint(1,200,(200,1))*1.0/10
    
    x = np.vstack((x0.T,x1.T,x2.T))
    #x = np.vstack((x0.T,x1.T))
    x = x.T
    
    objective = CdecAlignmentBLEUObjective()
    
    bo = BO(objective, noise=1e-1)

    fout = open('bo.reslut','w')
    for _ in xrange(1):
        bo.optimize(num_iters=1)

        # Get predictions for plotting
        #y_hat, y_hat_var = bo.predict(x, predict_variance=True)
        #y_hat_upper_bound = y_hat + 1.96 * np.sqrt(y_hat_var)
        #y_hat_lower_bound = y_hat - 1.96 * np.sqrt(y_hat_var)
        #ei = bo.expected_improvement(bo.grid)
        print 'Best Param:' + str(bo.best_param)
        print 'Best Value:' + str(bo.best_value)
        fout.write('iterations:'+ str(_)+'\n')
        fout.write(str(bo.best_param)+'\n')
        fout.write(str(bo.best_value)+'\n')
    fout.close()
    print "Optimization finished."
    print "Best parameter settings found:"
    # objective.map_params(...) will attach names to the parameters so you can tell what they are
    print(objective.map_params(bo.best_param))
    print "With cross validation accuracy: {}".format(bo.best_value)

    
