clear
./build/X86/gem5.opt --stats-file=${1}-${2}-${3}-${4}-${5}-${6}-${7}-${8}.txt ./configs/example/se.py  -n 8 --caches --l2cache --num-l2caches=8 --mem-size=4GB  --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU -F 25000  -I 250000 --bench $1-$2-${3}-${4}-${5}-${6}-${7}-${8}
