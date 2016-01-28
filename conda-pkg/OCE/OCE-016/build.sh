#! /bin/sh
set -e

backup_prefix=$PREFIX


# no longer used
#    GL2PS_INCLUDE_DIR
#    OPENCL_LIBRARIES

#      -DCMAKE_CXX_COMPILER=/usr/bin/c++ \

echo "Timestamp" && date
cmake -DOCE_ENABLE_DEB_FLAG:BOOL=OFF \
      -DCMAKE_BUILD_TYPE:STRING=Release \
      -DCMAKE_SYSTEM_PREFIX_PATH=$PREFIX \
      -DOCE_USE_TCL_TEST_FRAMEWORK:BOOL=OFF \
      -DOCE_VISUALISATION:BOOL=ON \
      -DOCE_OCAF:BOOL=ON \
      -DOCE_DRAW:BOOL=ON \
      -DOCE_INSTALL_CMAKE_DATA_DIR=lib \
      -DOCE_INSTALL_PACKAGE_LIB_DIR=$PREFIX/lib \
      -DOCE_DATAEXCHANGE:BOOL=ON \
      -DOCE_USE_PCH:BOOL=ON \
      -DOCE_WITH_GL2PS:BOOL=ON \
      -DGL2PS_INCLUDE_DIR=$PREFIX/include \
      -DOCE_MULTITHREAD_LIBRARY:STRING=TBB \
      -DOCE_TBB_MALLOC_SUPPORT=ON \
      -DTBB_INCLUDE_DIR=$PREFIX/include \
      -DOCE_WITH_FREEIMAGE:BOOL=ON \
      -DFREEIMAGE_INCLUDE_DIR=$PREFIX/include \
      -DOCE_RPATH_FILTER_SYSTEM_PATHS=ON \
      -DOCE_INSTALL_PREFIX=$PREFIX \
      -DOCE_TESTING=ON \
      $SRC_DIR

echo ""
echo "Timestamp" && date
echo "Starting build with -j $CPU_COUNT ..."
# travis-ci truncates when there are more than 10,000 lines of output.
# Builds generate around 9,000 lines of output, trim them to see test
# results.
make -j $CPU_COUNT | grep Built
make install

if [ `uname` != Darwin ]; then
    python $RECIPE_DIR/remove-system-libs.py $PREFIX/lib/OCE-libraries-release.cmake
fi

# Run OCE tests
# <<< FAILS FOR THE MOMENT >>>

#echo "Timestamp" && date
#make test

