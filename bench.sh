clear
./build/X86/gem5_bta_pref.opt --stats-file=${1}-${2}_bta_pref.txt ./configs/example/se.py  -n 2 --caches --l2cache  --mem-size=4GB  --mem-channels=1 --mem-ranks=8  --cpu-type=DerivO3CPU -F 25000  -I 250000 --bench $1-$2
