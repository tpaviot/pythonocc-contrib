#!/bin/bash

if [ "$PY3K" == "1" ]; then
    MY_PY_VER="${PY_VER}m"
else
    MY_PY_VER="${PY_VER}"
fi

if [ `uname` == Darwin ]; then
    PY_LIB="libpython${MY_PY_VER}.dylib"
else
    PY_LIB="libpython${MY_PY_VER}.so"
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
      -DPYTHON_INCLUDE_DIR:PATH=$PREFIX/include/python$MY_PY_VER \
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

# copy the examples to a /share folder
mkdir -p $PREFIX/share/pythonocc-core/examples
cp -r examples $PREFIX/share/pythonocc-core

echo "Done building and installing pythonocc-core" && date
