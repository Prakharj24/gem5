lbm lbm lbm lbm lbm lbm lbm lbm
clear
./build/X86/gem5.opt ./configs/example/se.py  -n 8 --caches --l2cache --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU --bench $1-$2-$3-$4-$5-$6-$7-$8
