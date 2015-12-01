
WORK-IN-PROGRESS:

* binstar integration is just a sketch
* build recipe is OK

OCE 0.17 matches OCC 6.8.0

OCE_INSTALL_PREFIX -> this needs to be set to Conda's prefix

for linux, use this channel for freeimage:
conda install -c https://conda.binstar.org/mutirri freeimage

perhaps run_test.py should run "make test", but that's a bit of a hassle. would be better if you can specify a shell script for testing

TODO:
* conda's [feature's](http://conda.pydata.org/docs/building/meta-yaml.html#features) would be a good idea to make 
for for instance a separate VTK enabled build...

