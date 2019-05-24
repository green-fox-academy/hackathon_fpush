cmake_minimum_required(VERSION 3.13)
project(finger)

set(CMAKE_CXX_STANDARD 17)



set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

set(OpenCV_FOUND 1)
find_package( OpenCV REQUIRED )

set(SOURCE_FILES main.cpp)

add_executable(fingers main.cpp)

target_link_libraries(finger ${OpenCV_LIBS})