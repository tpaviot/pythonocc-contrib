#! /bin/sh
set -e

# NOTE: OCE is build in debug mode only
# see issue https://github.com/tpaviot/oce/issues/576
# fix is available in OCC 7.0.0

COMPILER=CLANG # GCC
#
#if $COMPILER="CLANG" then
#      CXX_COMPILER=/usr/bin/clang++
#      C_COMPILER=/usr/bin/clang
#else
#      # no support for cocoa / objective-c with the conda GCC compiler suite
#      CXX_COMPILER=$PREFIX/bin/clang++
#      C_COMPILER=$PREFIX/bin/clang
#


echo "Timestamp" && date
cmake -DOCE_ENABLE_DEB_FLAG:BOOL=OFF \
      -DOCE_COPY_HEADERS_BUILD:BOOL=ON \
      -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
      -DCMAKE_C_COMPILER=/usr/bin/clang \
      -DCMAKE_CXX_FLAGS:STRING="-stdlib=libstdc++ " \
      -DCMAKE_BUILD_TYPE:STRING=Debug \
      -DCMAKE_OSX_DEPLOYMENT_TARGET="" \
      -DOCE_VISUALISATION:BOOL=ON \
      -DOCE_OCAF:BOOL=ON \
      -DOCE_DRAW:BOOL=ON \
      -DOCE_TBB_MALLOC_SUPPORT=ON \
      -DOCE_INSTALL_PACKAGE_LIB_DIR=$PREFIX/lib \
      -DTCL_INCLUDE_PATH=$PREFIX/include \
      -DTCL_LIBRARY=$PREFIX/lib/libtcl8.5.dylib \
      -DTCL_TCLSH=$PREFIX/bin/tclsh8.5 \
      -DTK_INCLUDE_PATH=$PREFIX/include \
      -DTK_LIBRARY=$PREFIX/lib/libtk8.5.dylib \
      -DTK_WISH=$PREFIX/bin/wish8.5 \
      -DOCE_DATAEXCHANGE:BOOL=ON \
      -DOCE_USE_PCH:BOOL=ON \
      -DOCE_WITH_GL2PS:BOOL=OFF \
      -DOCE_WITH_VTK:BOOL=OFF \
      -DVTK_DIR=$PREFIX/lib/cmake/vtk-6.2 \
      -DOCE_MULTITHREAD_LIBRARY:STRING=NONE \
      -DFREETYPE_LIBRARY=$PREFIX/lib/libfreetype.dylib \
      -DFREETYPE_INCLUDE_DIR_freetype2=$PREFIX/include/freetype2 \
      -DFREETYPE_INCLUDE_DIR_ft2build=$PREFIX/include \
      -DOCE_WITH_FREEIMAGE:BOOL=ON \
      -DFREEIMAGE_INCLUDE_DIR=$PREFIX/include \
      -DFREEIMAGE_LIBRARY=$PREFIX/lib/libfreeimage.a \
      -DOCE_INSTALL_PREFIX=$PREFIX \
      -DGL2PS_INCLUDE_DIR=$PREFIX/include \
      -DGL2PS_LIBRARY=$PREFIX/lib/libgl2ps.dylib \
      -DBUILD_TESTING=ON \
      -DOCE_TESTING=ON \
      -DOCE_USE_TCL_TEST_FRAMEWORK=OFF \
      $SRC_DIR

# ---> fuck you CMAKE, seriously, FUCK YOU

#      -DOCE_RPATH_FILTER_SYSTEM_PATHS=ON \
#      -DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \

# ---> ruling out that this has anything to do with a poorly built TBB lib

#      -DOCE_MULTITHREAD_LIBRARY:STRING=TBB \
#      -DTBB_INCLUDE_DIR=$PREFIX/include \
#      -DTBB_LIBRARY=$PREFIX/lib/libtbb.dylib  \
#      -DTBB_MALLOC_LIBRARY=$PREFIX/lib/libtbbmalloc.dylib \

# ---> CLANG

# issues with the current clang compiler:
# see https://github.com/tpaviot/oce/issues/576
#      -DCMAKE_CXX_FLAGS:STRING="-stdlib=libstdc++ " \

# ---> GCC

#      -DCMAKE_CXX_COMPILER=$PREFIX/bin/g++ \
#      -DCMAKE_C_COMPILER=$PREFIX/bin/gcc \

#      -DOCE_INSTALL_CMAKE_DATA_DIR=$PREFIX/lib \
#      -DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \

# vtk specific
# -undefined dynamic_lookup is needed to link the VTK stuff
#      -DCMAKE_CXX_FLAGS:STRING="-stdlib=libstdc++ -undefined dynamic_lookup" \
# some testing is done with X11, rendering it incompatible
#      -DOCE_DRAW:BOOL=OFF \


DYLD_FALLBACK_LIBRARY_PATH=$PREFIX/lib

echo ""
echo "Timestamp" && date
echo "Starting build with -j$ncpus ..."
# travis-ci truncates when there are more than 10,000 lines of output.
# Builds generate around 9,000 lines of output, trim them to see test
# results.
#make -j$CPU_COUNT | grep Built
make -j$CPU_COUNT

# test whether this build is any good
CTEST_OUTPUT_ON_FAILURE=1 make test

make install

# Run OCE tests
# <<< FAILS FOR THE MOMENT >>>

#echo "Timestamp" && date
#make test

