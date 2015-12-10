#!/bin/bash

# if you'd like to build a conda package from a local directory
# then comment out the "source" section in meta.yaml
# and replace $LOCAL_SRC_DIR to your pythonocc-core directory
#export LOCAL_SRC_DIR=/path/to/pythonocc-core/
#cp -r $LOCAL_SRC_DIR .

if [ `uname` == Darwin ]; then
    PY_LIB="libpython${PY_VER}.dylib"
else
    if [ "$PY3K" == "1" ]; then
        PY_LIB="libpython${PY_VER}m.so"
    else 
        PY_LIB="libpython${PY_VER}.so"
    fi
fi

echo "conda build directory is:" `pwd`
export PYTHONOCC_VERSION=`python -c "import OCC;print OCC.VERSION"`
echo "building pythonocc-core version:" $PYTHONOCC_VERSION


backup_prefix=$PREFIX

echo "Timestamp" && date
cmake -DCMAKE_INSTALL_PREFIX=$PREFIX \
      -DCMAKE_PREFIX_PATH=$PREFIX \
      -DCMAKE_SYSTEM_PREFIX_PATH=$PREFIX \
      -DCMAKE_BUILD_TYPE=Release \
      -DOCE_DIR=$PREFIX/lib \
      -DPYTHON_EXECUTABLE:FILEPATH=$PYTHON \
      -DPYTHON_INCLUDE_DIR:PATH=$PREFIX/include/python$PY_VER \
      -DPYTHON_LIBRARY:FILEPATH=$PREFIX/lib/${PY_LIB} \
      -DPYTHONOCC_INSTALL_DIRECTORY=$SP_DIR/OCC \
      -DPYTHONOCC_WRAP_DATAEXCHANGE=ON \
      -DPYTHONOCC_WRAP_OCAF=ON \
      -DPYTHONOCC_WRAP_VISU=ON \
      $SRC_DIR

echo ""
echo "Timestamp" && date
echo "Starting build with -j$ncpus ..."
make -j $CPU_COUNT
make install

# copy the swig interface files. There are software projects
# that might require these files to build own modules on top
# of pythonocc-core
mkdir -p $PREFIX/src
mkdir -p $PREFIX/src/pythonocc-core
cp -r src $PREFIX/src/pythonocc-core

echo "Done building and installing pythonocc-core" && date
