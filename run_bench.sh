clear
./build/X86/gem5.opt ./configs/example/se.py  -n 8 --caches --l2cache --mem-channels=1 --mem-ranks=8 --mem-size=4GB   --cpu-type=DerivO3CPU -F 1000000 -I 1000000  --bench $1-$2-$3-$4-$5-$6-$7-$8
