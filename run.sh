max=12
for i in `seq 0 $max`
do
    python load.py --fid $i --fname train
done
python combine_json.py --fname train

