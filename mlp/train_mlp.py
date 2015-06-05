
"""
usage train_mlp (previous pickled output)

This implements and trains a multi-layer percepteron which attempts to 
repoduces the cos theta star distributions from measurable data
save output at each epoch in MLPs folder

"""
__docformat__ = 'restructedtext en'


import os
import sys
import time
import pdb
import numpy
import sys
import theano
import theano.tensor as T
import matplotlib.pyplot as plt
from load_data import  load_data
from optparse import OptionParser

import cPickle
import random

global rng;
rng = numpy.random.RandomState(1234)

def plot_stat(pred,actual):
    values=actual-pred
    plt.figure(1)
    
    plt.subplot(2,1,1)
    plt.hist([i[0] for i in values],bins=50,range=(-1,1))
    plt.subplot(2,1,2)
    plt.hist([i[1] for i in values],bins=50,range=(-1,1))
    plt.draw()
    
    
    plt.figure(2)
    plt.clf()
    plt.subplot(2,1,1)
    
    
    max_v=max([max(i) for i in actual+pred])
    min_v=min([min(i) for i in actual+pred])
    
    plt.hist([i[0] for i in actual],bins=50,range=(min_v,max_v))
    plt.hist([i[0] for i in pred],bins=50,range=(min_v,max_v))
    plt.subplot(2,1,2)
    plt.hist([i[1] for i in actual],bins=50,range=(min_v,max_v))
    plt.hist([i[1] for i in pred],bins=50,range=(min_v,max_v))

    min_v=-1
    max_v=1
#    plt.figure(3)
#    plt.hist2d([i[0] for i in pred],[i[1] for i in pred],bins=20,range=((min_v,max_v),(min_v,max_v)))

#    plt.figure(4)
#    plt.hist2d([i[0] for i in actual],[i[1] for i in actual],bins=20,range=((min_v,max_v),(min_v,max_v)))

    plt.draw()    
#    plt.draw()
        




# start-snippet-1
class Layer(object):
    def __init__(self, layer_num, input_v, n_in, n_out, W=None, b=None,
                 activation=T.tanh):
        global rng
        if W is None:
            W_values = numpy.asarray(
                rng.uniform(
                    low=-numpy.sqrt(6. / (n_in + n_out)),
                    high=numpy.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)
                ),
                dtype=theano.config.floatX
            )
            if activation == theano.tensor.nnet.sigmoid:
                W_values *= 4
            W = theano.shared(value=W_values, name='W'+str(layer_num), borrow=True)
        if b is None:
            b_values = numpy.zeros((n_out,), dtype=theano.config.floatX)
            b = theano.shared(value=b_values, name='b'+str(layer_num), borrow=True)
        self.W = W
        self.b = b

        lin_output = T.dot(input_v, self.W) + self.b
        if activation:
            self.output =activation(lin_output)
        else:
            self.output=lin_output
        # parameters of the model
        self.params = [self.W, self.b]
        self.cost=self.err_sqr

    def err_sqr(self,y):
#        pdb.set_trace()
        dv=self.output-y
        return T.mean((T.sum((dv**2),1)))**.5


# start-snippet-2
class MLP:

    def __init__(self, input_v, n_in, n_hidden, n_out,n_layer):
        print "bulding MLP with ", n_layer," hidden layers with ",n_hidden," nodes"
        self.n_hidden=n_hidden
        self.n_layer=n_layer
        self.n_in=n_in
        self.n_out=n_out
        self.input_v=input_v

        self.H_layers=[]
        for i in range(n_layer):
            if i==(n_layer-1) and i!=0: #last layer
                print n_in
                n_ins=n_hidden
                n_out=2
                inv=self.H_layers[i-1].output 
                activation=None
            elif i==(n_layer-1) and i==0: #last and only layer
                n_ins=n_in
                n_out=2
                inv=input_v
                activation=None
            elif i==0: #first layer
                print n_in
                n_ins=n_in
                n_out=n_hidden
                inv=input_v
                activation=T.tanh
            else: # normal layer
                n_ins=n_hidden
                n_out=n_hidden
                inv=self.H_layers[i-1].output 
                activation=T.tanh   
            self.H_layers.append(Layer(
                i,
                inv,
                n_in=n_ins,
                n_out=n_out,
                activation=activation
            ))
 

    
        self.errors = self.H_layers[-1].err_sqr
        self.cost = self.H_layers[-1].err_sqr
        self.output = self.H_layers[-1].output

        # the parameters of the model are the parameters of the two layer it is
        # made out of
        self.params =  []
        for H in self.H_layers:
            self.params+=H.params
    def __getinitargs__(self):
        return self.input_v, self.n_in, self.n_hidden, self.n_out, self.n_layer
            
    def __getstate__(self):
        layer_data=[h.params for h in self.H_layers]
        return layer_data
    
    def __setstate__(self,state):
        layer_data=state
        for h,d in zip(self.H_layers,layer_data):
            h.W.set_value(d[0].get_value())
            h.b.set_value(d[1].get_value())
            
        

#-3 best so far -4 about the same -5 is bad
def test_mlp(learning_rate=1*10**-4, L1_reg=0.00, L2_reg=0.0001, n_epochs=10000,
             dataset='mnist.pkl.gz', batch_size=50,n_hidden=200,n_layer=20,out_name="",in_class=None):

    datasets = load_data(dataset)

    train_set_x, train_set_y = datasets[0]
    valid_set_x, valid_set_y = datasets[1]
    test_set_x, test_set_y = datasets[2]

    # compute number of minibatches for training, validation and testing
    n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size
    n_valid_batches = valid_set_x.get_value(borrow=True).shape[0] / batch_size
    n_test_batches = test_set_x.get_value(borrow=True).shape[0] / batch_size

    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print '... building the model'

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch
    x = T.matrix('x')  # the data is presented as rasterized images
    y = T.matrix('y')  # the labels are presented as 1D vector of
                        # [int] labels


    # construct the MLP class
    if in_class==None:
        classifier = MLP(
            input_v=x,
            n_in=14,
            n_hidden=n_hidden,
            n_out=2,
            n_layer=n_layer
        
        )
    else:
        classifier=cPickle.load(open(in_class,"rb"))
        x=classifier.input_v
        

    # start-snippet-4
    # the cost we minimize during training is the negative log likelihood of
    # the model plus the regularization terms (L1 and L2); cost is expressed
    # here symbolically
    cost = (
        classifier.cost(y)
    )
    errors = (
        classifier.errors(y)
    )

    test_model = theano.function(
        inputs=[index],
        outputs=classifier.errors(y),
        givens={
            x: test_set_x[index * batch_size:(index + 1) * batch_size],
            y: test_set_y[index * batch_size:(index + 1) * batch_size]
        }
    )

    validate_model = theano.function(
        inputs=[index],
        outputs=classifier.errors(y),
        givens={
            x: valid_set_x[index * batch_size:(index + 1) * batch_size],
            y: valid_set_y[index * batch_size:(index + 1) * batch_size]
        }
    )

    # start-snippet-5
    # compute the gradient of cost with respect to theta (sotred in params)
    # the resulting gradients will be stored in a list gparams

    gparams = [T.grad(cost, param) for param in classifier.params]

    # specify how to update the parameters of the model as a list of
    # (variable, update expression) pairs

    # given two list the zip A = [a1, a2, a3, a4] and B = [b1, b2, b3, b4] of
    # same length, zip generates a list C of same size, where each element
    # is a pair formed from the two lists :
    #    C = [(a1, b1), (a2, b2), (a3, b3), (a4, b4)]
    updates = [
        (param, param - learning_rate * gparam)
        for param, gparam in zip(classifier.params, gparams)
    ]

    # compiling a Theano function `train_model` that returns the cost, but
    # in the same time updates the parameter of the model based on the rules
    # defined in `updates`
    train_model = theano.function(
        inputs=[index],
        outputs=cost,
        updates=updates,
        givens={
            x: train_set_x[index * batch_size: (index + 1) * batch_size],
            y: train_set_y[index * batch_size: (index + 1) * batch_size]
        }
    )
    # end-snippet-5

    ###############
    # TRAIN MODEL #
    ###############
    print '... training'

    # early-stopping parameters
    patience = 10000  # look as this many examples regardless
    patience_increase = 4  # wait this much longer when a new best is
                           # found
    improvement_threshold = 0.995  # a relative improvement of this much is
                                   # considered significant
    validation_frequency = min(n_train_batches, patience / 2)
                                  # go through this many
                                  # minibatche before checking the network
                                  # on the validation set; in this case we
                                  # check every epoch

    best_validation_loss = numpy.inf
    best_iter = 0
    test_score = 0.
    start_time = time.clock()

    epoch = 0
    done_looping = False
#    pdb.set_trace()
    while (epoch < n_epochs) and (not done_looping):
#        for i in classifier.params:
#            print i.get_value()

        cPickle.dump(classifier,open(out_name+"_"+str(epoch)+".pkl","wb"))

        epoch = epoch + 1

        pred=classifier.output.eval({x:test_set_x.get_value()})
        actual=test_set_y.get_value()
        plot_stat(pred,actual)
        
        for minibatch_index in xrange(n_train_batches):

            minibatch_avg_cost = train_model(minibatch_index)
            # iteration number
#            pred=classifier.output.eval({x:test_set_x.get_value()})
#            actual=test_set_y.get_value()
#            values=actual-pred
#            pdb.set_trace()

            iter = (epoch - 1) * n_train_batches + minibatch_index

            if (iter + 1) % validation_frequency == 0:
                # compute zero-one loss on validation set
                validation_losses = [validate_model(i) for i
                                     in xrange(n_valid_batches)]
                this_validation_loss = numpy.mean(validation_losses)

                print(
                    'epoch %i, minibatch %i/%i, validation error %f %%' %
                    (
                        epoch,
                        minibatch_index + 1,
                        n_train_batches,
                        this_validation_loss * 100.
                    )
                )

                # if we got the best validation score until now
                if this_validation_loss < best_validation_loss:
                    #improve patience if loss improvement is good enough
                    if (
                        this_validation_loss < best_validation_loss *
                        improvement_threshold
                    ):
                        patience = max(patience, iter * patience_increase)

                    best_validation_loss = this_validation_loss
                    best_iter = iter

                    # test it on the test set
                    test_losses = [test_model(i) for i
                                   in xrange(n_test_batches)]
                    test_score = numpy.mean(test_losses)

                    print(('     epoch %i, minibatch %i/%i, test error of '
                           'best model %f %%') %
                          (epoch, minibatch_index + 1, n_train_batches,
                           test_score * 100.))

            if patience <= iter:
                done_looping = True
                break

    end_time = time.clock()
    print(('Optimization complete. Best validation score of %f %% '
           'obtained at iteration %i, with test performance %f %%') %
          (best_validation_loss * 100., best_iter + 1, test_score * 100.))
    print >> sys.stderr, ('The code for file ' +
                          os.path.split(__file__)[1] +
                          ' ran for %.2fm' % ((end_time - start_time) / 60.))

    cPickle.dump(classifier,open(out_name+"_"+str(epoch)+".pkl","wb"))
    #out_f=open("params.out","w")
    #cPickle.dump(classifier)
    #out_f.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--infile", dest="in_file",
                      help="input template file", default=None)
    parser.add_option("-o", "--out_tag", dest="out_tag",
                      help="Out_tag_for training", default="MLPs/real_5")

    parser.add_option("--lr", dest="learning_rate",type="float",
                      help="learning_rate", default=.001)

    parser.add_option("--hu", dest="hidden_units",type="float",
                      help="hidden units", default=200)
    parser.add_option("--hl", dest="hidden_layers",type="float",
                      help="hidden layers", default=20)

    (options, args) = parser.parse_args()

    
    try:in_class=sys.argv[1]
    except: in_class=None
    test_mlp(out_name=options.out_tag,in_class=options.in_file,learning_rate=options.learning_rate,n_hidden=options.hidden_units,n_layer=options.hidden_layers)
