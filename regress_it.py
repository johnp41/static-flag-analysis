import pickle
import subprocess
import numpy as np
import os

"""
    input:takes array of features
    output: list where each item is compination of flags(binarized)+features array

"""
def add_flags(arr):
    with open('dict_flags','rb') as dict_flags:
        dict_flags = pickle.load(dict_flags)
    with open('rev_dict_flags','rb') as rev_dict:
        rev_dict = pickle.load(rev_dict)
    #binary flags
    bin_flags = []
    for i in dict_flags.values():
        bin_flags.append('{0:012b}'.format(i))
    # bin flags list apo listes apo digits pou represnt flags
    bin_flags = [list(map(int,x)) for x in bin_flags]
    flaged= []
    for i in range(len(bin_flags)):
        flaged.append(list(arr[0]) + bin_flags[i])
    flaged = np.array(flaged)
    return flaged

"""
    input:array of features
    output:scaled array of features (for regress)
"""
def scale_it(arr):
    with open('scaler','rb') as scaler:
        scaler = pickle.load(scaler)
        arr=np.array(arr)
        arr = arr.reshape(1,-1)
        arr=scaler.transform(arr)
        return arr 

"""
    input:list of scaled features+ flags
    output : list of speedup prediction
"""
def get_preds(arr,st):
    with open('reg'+st,'rb') as reg:
        reg = pickle.load(reg)
    pred=[]
    for x in arr.tolist():
        x = np.array(x).reshape(1,-1)
        pred.append(reg.predict(x)[0])
#    with open('my_scaled','wb') as fille:
#        pickle.dump(x,fille)
    return pred

"""
    input : list of predicted speedups
    output : best flag combination
"""
def find_best_flags(preds):
    #dict[index]-->flag combination
    with open('rev_dict_flags','rb') as rev_dict:
        rev_dict = pickle.load(rev_dict)
    n =5
    lista = sorted(range(len(preds)),key =lambda ind : preds[ind],reverse=True)
    print(15*'=','Best prediction-flags',15*'=')
    for i in range(n):
#        print('Pred : ', preds[lista[i]] ,'Flag ' , rev_dict[lista[i]] )
        print('Flag ' , rev_dict[lista[i]] )       
    return (rev_dict[lista[0]])

"""
    modifies str in appropriate form
"""
def stringify(flags):
    flags=flags.split("-")
    flags2 =""
    for n,i in enumerate(flags) :    
        if i == 'unroll':
            del flags[n]
        if i=='loop':
            flags[n]='loop-unroll'
    for i in flags:
        flags2+='-'+str(i)+" "
    return flags2


"""
    input: arr of features
    output: list of best compination of flags
"""
def regress(arr,st='O3'):
    assert (st == 'O3' or st=='O2' or st == 'O0') ,'wrong Flag'
    #open the regressor 
    with open('reg'+st ,'rb') as reg:
        reg = pickle.load(reg)
        arr = add_flags(arr)
        preds=get_preds(arr,st)
        flags =find_best_flags(preds)
        return flags

"""
    takes list of flags and compiles
"""
def compile(flags):
    flags = stringify(flags)
    comp="clang-7 -emit-llvm -Xclang -disable-O0-optnone -Wno-everything -c *.c"
    link="llvm-link-7 -S *.bc -o basic.ll"
    opt ="opt-7 " + flags + " basic.ll -S -o new.ll"
    llc="llc-7 new.ll"
    clang="clang-7 new.s -lm -o a.out"
    subprocess.check_output(comp,shell=True)
    subprocess.check_output(link,shell=True)
    subprocess.check_output(opt,shell=True)
    subprocess.check_output(llc,shell=True)
    subprocess.check_output(clang,shell=True)
    print("compiled with "+flags)
