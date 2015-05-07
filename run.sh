cd lhe_converter

if [[ -s run-convert.exe ]]
then
echo "building lhe converter"
make
fi

cd ../

cd mlp
if [[ -s ./data/WWdata_ct2.pkl.gz ]]
then
echo "Missing Theano data creating"
python root_to_data.py ../data/Output_sm.root 
fi
echo "building templates"
python make_templates.py


cd ../


