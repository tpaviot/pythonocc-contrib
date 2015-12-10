#! /bin/bash

set -e

mkdir cmake-build
cd cmake-build

cmake -DBoost_DIR=$PREFIX/share/cmake-3.0/Modules/ \
      -DBoost_INCLUDE_DIR=$PREFIX/include \
      -DCMAKE_BUILD_TYPE:STRING=Release \
      -DOCE_DIR=$PREFIX/lib \
      -DSMESH_TESTING=ON \
      -DCMAKE_INSTALL_PREFIX=$PREFIX \
      $SRC_DIR

# travis-ci truncates when there are more than 10,000 lines of output.
# trim them to see test results.
make -j $CPU_COUNT install | grep Built
