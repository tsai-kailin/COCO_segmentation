max=12
for i in `seq 0 $max`
do
    python load.py --fid $i --fname train2017
done
python combine_json.py --fname train2017

python convert_mask.py --fname train2017