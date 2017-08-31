clear
./build/X86/gem5.opt --stats-file=${3} ./configs/example/se.py  -n 2 --caches --l2cache --mem-size=4GB  --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU -F 1000000 -I 10000  --bench $1-$2
