#! /usr/bin/python

## Modifications to Eleni's code for the runtime performance study

from __future__ import print_function
import logging
import networkx as nx
from lomap import Fsa, Ts, Wfse, ts_times_wfse_times_fsa
from lomap import Timer
import time
import matplotlib.pyplot as plt


def fsa_constructor(n):

    print("i",n)

    # Define the set ofatomic propositions
    # ap = set(['fd','w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'co', 'w7', 'w8', 'w9','w10','w11', 'w12', 'w13', 'w14', 'w15', 'w16', 'w17', 'w18', 'w19', 'w20' ]) #'w21','w22', 'w23', 'w24']) # set of atomic propositions // MODIFY

    ap = set(['fd','w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7','co']) 

    # ap = set(['FD','B1', 'B2', 'B3', 'B4','B5', 'B6', 'CO'])

 
    specs = 'F w1'


    for j  in range (2,n): 

        specs = specs + '& X w{}'.format(j+1) + '| ! w{}'.format(j)
        # specs = specs + '& X w2'


    specification = ([specs])


    fsa = Fsa(props=ap, multi=False) # empty FSA with propsitions from `ap`
    for spec in specification:
        fsa.from_formula(spec)

    print("fsa_nodes:",fsa.g.number_of_nodes())

    print("fsa_edges:",fsa.g.number_of_edges())

    print(specs)


    return fsa

#TS
#MODIFY THE TS: Vary the size of the TS instead of FSA/WFSE

def ts_constructor():
    # using a loop to make it easier for the programmer to modify the size of the ts (add nodes)
    ts = Ts(directed=True, multi=False)
    #establishing the size of the grid (different in each iteration)
    # print("ts", ts.g)

    n_ts_rows = 2
    n_ts_columns = 4
    ts.g = nx.grid_2d_graph(n_ts_rows,n_ts_columns)    
    ts.init[(0,0)] = 1

    fd_row = 0
    fd_col = 0
    co_row = n_ts_rows-1
    co_col = n_ts_columns-1

    #modify the limits of the range for different sizes
    #add the initial and final nodes
    ts.g.add_node((fd_row,fd_col), attr_dict={'prop': set('fd')}) #initial state: front desk

    # ts.g[fd_row][fd_col]['prop'] = set('fd')
    ts.g.add_node((co_row,co_col), attr_dict={'prop': set(['co'])}) #modify according to which number the final state is for the different sizes


    #adding nodes for the books
    ts.g.add_node(((0,1)), attr_dict={'prop': set(['w1'])})
    ts.g.add_node(((0,2)), attr_dict={'prop': set(['w2'])})
    ts.g.add_node(((0,3)), attr_dict={'prop': set(['w3'])})
    # ts.g.add_node(((0,4)), attr_dict={'prop': set(['w4'])})
    # ts.g.add_node(((0,5)), attr_dict={'prop': set(['w5'])})
    # ts.g.add_node(((0,6)), attr_dict={'prop': set(['w6'])})
    # ts.g.add_node(((0,7)), attr_dict={'prop': set(['w7'])})
    # ts.g.add_node(((0,8)), attr_dict={'prop': set(['w8'])})
    # ts.g.add_node(((0,9)), attr_dict={'prop': set(['w9'])})
    # ts.g.add_node(((0,10)), attr_dict={'prop': set(['w10'])})
    ts.g.add_node(((1,0)), attr_dict={'prop': set(['w4'])})
    ts.g.add_node(((1,1)), attr_dict={'prop': set(['w5'])})
    ts.g.add_node(((1,2)), attr_dict={'prop': set(['w6'])})
    ts.g.add_node(((1,3)), attr_dict={'prop': set(['w7'])})
    # ts.g.add_node(((1,4)), attr_dict={'prop': set(['w15'])})
    # ts.g.add_node(((1,5)), attr_dict={'prop': set(['w16'])})
    # ts.g.add_node(((1,6)), attr_dict={'prop': set(['w17'])})
    # ts.g.add_node(((1,7)), attr_dict={'prop': set(['w18'])})
    # ts.g.add_node(((1,8)), attr_dict={'prop': set(['w19'])})
    # ts.g.add_node(((1,9)), attr_dict={'prop': set(['w20'])})

    # nx.set_node_attributes(graph, name='prop', values=3.0)

    #adding the edges from each book to intial and to final states
    for x in range(0,n_ts_columns):
        for y in range(0,n_ts_columns):
            if (x == 0 & y == 0):
                continue
            elif(x == co_row & y == co_col):
                continue
            ts.g.add_edge((0,0), (x,y) ,weight=1)
            ts.g.add_edge((x,y), (co_row,co_col) ,weight=1)            


            ts.g.add_edge((x,y), (x+1,y+1) ,weight=1)


    # ts.g.add_edge((0,3), (1,0) ,weight=1)
    ts.g.add_edge((0,1), (0,2) ,weight=1)

    ts.g.add_edge((0,3), (1,0), weight=1)
    


    ts.g.add_edges_from((u, u) for u in ts.g) # self-loop
    
    ts.g.add_edges_from(ts.g.edges(), weight=1)

    print("ts_nodes: ", ts.g.number_of_nodes())
    print("ts_edges: ", ts.g.number_of_edges())

    return ts

    
#WFSE
def wfse_constructor():
    # ap = set(['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'co', 'w7', 'w8', 'w9','w10', 'w11', 'w12', 'w13', 'w14', 'w15', 'w16', 'w17', 'w18', 'w19', 'w20', 'co']) 
    ap = set(['fd','w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7','co']) 

    wfse = Wfse(props=ap, multi=False)
    wfse.init = set() # HACK
    
    # add states
    # wfse.g.add_nodes_from(['fd', 'q1', 'q2', 'q3', 'q4','q5','q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12','q13','q14','q15', 'q16','q17','q18', 'q19', 'q20', 'co', ]) 
    wfse.g.add_nodes_from(['fd', 'q1', 'q2', 'q3', 'q4','q5','q6','co' ]) 

    # add transitions
    pass_through_symbols = [(symbol, symbol, 1) for symbol in wfse.prop_bitmaps
                            if symbol >= 0]
    #print('pass through symbols:', pass_through_symbols) # THIS TAKES A WHILE TO PRINT
    wfse.g.add_edge('fd', 'fd', attr_dict={'symbols': pass_through_symbols})
    wfse.g.add_edge('co', 'co', attr_dict={'symbols': pass_through_symbols})
    

    # book = int(book)

    state_prev = 'fd'

    count = 1

    # state = 'q{}'.format(1 )


    book_str = 'w{}'.format(2) #substitute with the next book
    in_symbol = wfse.bitmap_of_props(set([book_str]))
    book_str = 'w{}'.format(1)
    # book_str = 'w1'
    out_symbol = wfse.bitmap_of_props(set([book_str]))
    weighted_symbols = [(in_symbol, out_symbol, 1)]

    wfse.g.add_edge('fd', 'q1', attr_dict={'symbols': weighted_symbols})

    wfse.g.add_edge('q1', 'q2', attr_dict={'symbols': weighted_symbols})


    # book_str = 'w{}'.format(3) #substitute with the next book
    # in_symbol = wfse.bitmap_of_props(set([book_str]))
    # book_str = 'w{}'.format(1)
    # # book_str = 'w1'
    # out_symbol = wfse.bitmap_of_props(set([book_str]))
    # weighted_symbols = [(in_symbol, out_symbol, 1)]

    # wfse.g.add_edge('q2', 'q3', attr_dict={'symbols': weighted_symbols})


    # out_symbol = wfse.bitmap_of_props(set(['w{}'.format(book)]))
    weighted_symbols = [( out_symbol, -1, 2)]
    wfse.g.add_edge('q2', 'co', attr_dict={'symbols': weighted_symbols})



    
    # set the initial state
    wfse.init.add('fd')
    # set the final state
    wfse.final.add('co')



    print("wfse_nodes: ", wfse.g.number_of_nodes())
    print("wfse_edges: ", wfse.g.number_of_edges())
    
    return wfse

def main():
    logging.basicConfig(level=logging.DEBUG)
    # print("Please enter the book number")
    # book = str(input())

    product_size = [] 
    pa_construct = []
    fsa_size = [] 
    # control_synthesis = []



    n = 7

    for k in range (1,n): 

        fsa = fsa_constructor(k)

        ts = ts_constructor()

        wfse = wfse_constructor()

        pa_start = time.time()
        with Timer('Product construction'):
           product_model = ts_times_wfse_times_fsa(ts, wfse, fsa)

        pa_end = time.time()


        #print(product_model.g.edges())
        # print('Product: Init:', product_model.init) # initial states
        # print('Product: Final:', product_model.final) # final 


        print("pa_nodes: ", product_model.g.number_of_nodes())
        print("pa_edges: ", product_model.g.number_of_edges())
        print('Product: Size', product_model.size()) # number of states and transitions

        product_size.append(product_model.g.number_of_nodes())
        fsa_size.append(fsa.g.number_of_nodes())
        pa_construct.append(pa_end - pa_start)

        # print("time:", pa_construct)
        # print(wfse_size)
        print(product_size)

    fig1,ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    ax.plot(fsa_size, pa_construct, 'bo',label='pa_construction', linewidth=3)
    ax2.plot(fsa_size, product_size, 'c-', label = 'pa_size', linewidth=3)
    ax2.set_xlabel('FSA Size', fontsize=16)
    ax2.set_ylabel('pa_size', fontsize=16)

    plt.grid(b=True)
    ax2.legend(fontsize=15)
    plt.show()


if __name__ == '__main__':
    main()

