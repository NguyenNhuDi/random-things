cmake_minimum_required(VERSION 3.23)
project(KernelPractic LANGUAGES CXX HIP)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (NOT DEFINED GPU_TARGETS)
  set(GPU_TARGETS "all" CACHE STRING "GPU architectures to compile for")
endif()
set_property(CACHE GPU_TARGETS PROPERTY STRINGS "all")

set(CMAKE_HIP_ARCHITECTURES ${GPU_TARGETS})
include(FetchContent)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.15.2   # pin a tag; never track a moving branch
)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()
include(GoogleTest)

function(add_exe name)
  add_executable(${name} ${name}.cpp)
  set_source_files_properties(${name}.cpp PROPERTIES LANGUAGE HIP)
  target_include_directories(${name} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
  target_link_libraries(${name} PRIVATE GTest::gtest_main)
  gtest_discover_tests(${name})
endfunction()

add_exe(vector_addition)
add_exe(block_exchange)


