mkdir build
cd build

REM Remove dot from PY_VER for use in library name
set MY_PY_VER=%PY_VER:.=%

REM Configure step
cmake -G "Ninja" -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%" ^
 -DCMAKE_BUILD_TYPE=Release ^
 -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%" ^
 -DCMAKE_SYSTEM_PREFIX_PATH="%LIBRARY_PREFIX%" ^
 -DPYTHON_EXECUTABLE:FILEPATH="%PYTHON%" ^
 -DPYTHON_INCLUDE_DIR:PATH="%PREFIX%"/include ^
 -DPYTHON_LIBRARY:FILEPATH="%PREFIX%"/libs/python%MY_PY_VER%.lib ^
 -DPYTHONOCC_INSTALL_DIRECTORY=%SP_DIR%/OCC ^
 -DPYTHONOCC_WRAP_DATAEXCHANGE=ON ^
 -DPYTHONOCC_WRAP_OCAF=ON ^
 -DPYTHONOCC_WRAP_VISU=ON ^
 ..
if errorlevel 1 exit 1
 
REM Build step 
ninja
if errorlevel 1 exit 1

REM Install step
ninja install
if errorlevel 1 exit 1

REM copy the swig interface files. There are software projects
REM that might require these files to build own modules on top
REM of pythonocc-core
cd ..
xcopy src "%LIBRARY_PREFIX%\src\pythonocc-core\src" /s /e /i
if errorlevel 1 exit 1