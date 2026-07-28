#pragma once

#include <gtest/gtest.h>
#include <hip/hip_runtime.h>

#include <algorithm>
#include <concepts>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <random>
#include <utility>

#define CEIL_DIV(a, b) (a + b - 1) / b;

#define HIP_CHECK(cmd)                                                   \
  do {                                                                   \
    auto error = (cmd);                                                  \
    if (error != hipSuccess) {                                           \
      std::cerr << "Encountered HIP error (" << hipGetErrorString(error) \
                << ") at line " << __LINE__ << " in file " << __FILE__   \
                << "\n";                                                 \
      exit(-1);                                                          \
    }                                                                    \
  } while (0)

template <class T>
struct distribution_selector {
  template <class I>
    requires std::integral<I>
  static auto test(I) -> std::uniform_int_distribution<I>;

  template <class F>
    requires std::floating_point<F>
  static auto test(F) -> std::uniform_real_distribution<F>;

  using type = decltype(test(std::declval<T>()));
};

template <typename T>
T get_min() {
  return std::numeric_limits<T>::min();
}

template <typename T>
T get_max() {
  return std::numeric_limits<T>::max();
}