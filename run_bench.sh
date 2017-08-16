clear
./build/X86/gem5.opt ./configs/example/se.py  -n 8 --caches --l2cache --mem-size=4GB  --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU -F 5000 -I 10000  --bench $1-$2-$3-$4-$5-$6-$7-$8

