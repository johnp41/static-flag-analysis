import sys 
import os 
import pathlib
import shutil
import subprocess
from collector import collect
from regress_it import *

"""
    main drriver
"""
def main():
    file_name = sys.argv[1]
    folder_name = sys.argv[1][:-2]
    files_list= [x for x in sys.argv[1:]]
    if not(os.path.exists(folder_name)):
        os.mkdir(folder_name)
    for x in files_list:
        shutil.copy(x,folder_name)
    os.chdir(folder_name)
    #docker stuff i need to read
    dock= "sudo docker run --mount type=bind,src=$(pwd),dst=/sources -ti lullo/milepost-feature-extractor:slim"
    # change owner from root of docker files 
    chown= "sudo chown $(id -u) ./features*"
    subprocess.call(dock,shell=True)
    subprocess.call(chown,shell=True)
    os.chdir('features')
    feat_arr = collect()
    feat_arr = scale_it(feat_arr)
    ##regress pacjkage her
    lista = regress(feat_arr)
    os.chdir(folder_name)
    compile(lista)
    os.chdir('../')
##    shutil.rmtree(folder_name)

if __name__ == '__main__':
    main()
