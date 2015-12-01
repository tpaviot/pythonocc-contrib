
WORK-IN-PROGRESS:

* unreleased OCE version, [see this branch](https://github.com/blobfish/oce/tree/691patched_2)
* note this branch is a pull request ( 01-12-2015 ), so by now this might be releaased
* VTK integration doesnt work
* binstar integration is just a sketch
* build recipe is OK



OCE 0.18 -> OCC 6.9.1

OCE_INSTALL_PREFIX -> this needs to be set to Conda's prefix

for linux, use this channel for freeimage:
conda install -c https://conda.binstar.org/mutirri freeimage

perhaps run_test.py should run "make test", but that's a bit of a hassle. would be better if you can specify a shell script for testing

TODO:
* conda's [feature's](http://conda.pydata.org/docs/building/meta-yaml.html#features) would be a good idea to make 
for for instance a separate VTK enabled build...

