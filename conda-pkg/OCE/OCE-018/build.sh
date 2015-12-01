#! /bin/sh
set -e

# NOTE: OCE is build in debug mode only
# see issue https://github.com/tpaviot/oce/issues/576
# fix is available in OCC 7.0.0

echo "Timestamp" && date
cmake -DOCE_ENABLE_DEB_FLAG:BOOL=OFF \
      -DCMAKE_BUILD_TYPE:STRING=Debug \
      -DCMAKE_OSX_DEPLOYMENT_TARGET="" \
      -DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \
      -DCMAKE_CXX_FLAGS:STRING="-stdlib=libstdc++ " \
      -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
      -DCMAKE_C_COMPILER=/usr/bin/clang \
      -DOCE_VISUALISATION:BOOL=ON \
      -DOCE_OCAF:BOOL=ON \
      -DOCE_DRAW:BOOL=ON \
      -DOCE_TESTING=ON \
      -DBUILD_TESTING=ON \
      -DOCE_USE_TCL_TEST_FRAMEWORK=OFF \
      -DOCE_INSTALL_CMAKE_DATA_DIR=lib \
      -DOCE_INSTALL_PACKAGE_LIB_DIR=$PREFIX/lib \
      -DOCE_DATAEXCHANGE:BOOL=ON \
      -DOCE_USE_PCH:BOOL=ON \
      -DOCE_WITH_GL2PS:BOOL=OFF \
      -DOCE_WITH_VTK:BOOL=OFF \
      -DOCE_WITH_FREEIMAGE:BOOL=ON \
      -DOCE_MULTITHREAD_LIBRARY:STRING=TBB \
      -DOCE_TBB_MALLOC_SUPPORT=ON \
      -DOCE_RPATH_FILTER_SYSTEM_PATHS=ON \
      -DOCE_INSTALL_PREFIX=$PREFIX \
      -DTCL_INCLUDE_PATH=$PREFIX/include \
      -DTCL_LIBRARY=$PREFIX/lib/libtcl8.5.dylib \
      -DTCL_TCLSH=$PREFIX/bin/tclsh8.5 \
      -DTK_INCLUDE_PATH=$PREFIX/include \
      -DTK_LIBRARY=$PREFIX/lib/libtk8.5.dylib \
      -DTK_WISH=$PREFIX/bin/wish8.5 \
      -DFREETYPE_LIBRARY=$PREFIX/lib/libfreetype.dylib \
      -DFREETYPE_INCLUDE_DIR_freetype2=$PREFIX/include/freetype2 \
      -DFREETYPE_INCLUDE_DIR_ft2build=$PREFIX/include \
      -DFREEIMAGE_INCLUDE_DIR=$PREFIX/include \
      -DFREEIMAGE_LIBRARY=$PREFIX/lib/libfreeimage.a \
      -DTBB_INCLUDE_DIR=$PREFIX/include \
      -DTBB_LIBRARY=$PREFIX/lib/libtbb.dylib  \
      -DTBB_MALLOC_LIBRARY=$PREFIX/lib/libtbbmalloc.dylib \
      -DVTK_DIR=$PREFIX/lib/cmake/vtk-6.2 \
      -DGL2PS_INCLUDE_DIR=$PREFIX/include \
      -DGL2PS_LIBRARY=$PREFIX/lib/libgl2ps.dylib \
      $SRC_DIR



echo ""
echo "Timestamp" && date
echo "Starting build with -j$ncpus ..."
# travis-ci truncates when there are more than 10,000 lines of output.
# Builds generate around 9,000 lines of output, trim them to see test
# results.
#  make -j$CPU_COUNT | grep Built
make -j$CPU_COUNT

# test whether this build is any good
#CTEST_OUTPUT_ON_FAILURE=1 make test

make install

#echo "Timestamp" && date
#make test

