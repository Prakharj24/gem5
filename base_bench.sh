clear
./build/X86/gem5_base_pref.opt --stats-file=${1}-${2}_base_pref.txt ./configs/example/se.py  -n 2 --caches --l2cache --mem-size=4GB  --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU -F 250000000  -I 250000000 --bench $1-$2
