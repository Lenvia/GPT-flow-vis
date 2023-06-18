mkdir build
cd build
cmake -DCMAKE_TOOLCHAIN_FILE=/Users/yy/vcpkg/scripts/buildsystems/vcpkg.cmake ..
cmake --build . -- -j