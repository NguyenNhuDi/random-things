#include "util.hpp"

template <typename T>
__global__ void vec_add(const T *a, const T *b, T *c, const size_t N) {
  const size_t bIdx = blockIdx.x, tIdx = threadIdx.x;
  const size_t idx = tIdx + bIdx * blockDim.x;

  if (idx < N) c[idx] = a[idx] + b[idx];
}

using VectorAdditionParams = ::testing::Types<int32_t, uint32_t, float, double>;

template <typename T>
struct VectorAddition : public ::testing::Test {
  using type = T;
  std::vector<size_t> sizes = {512, 2048, 18'217};
};

TYPED_TEST_SUITE(VectorAddition, VectorAdditionParams);

TYPED_TEST(VectorAddition, Basic) {
  auto sizes = TestFixture::sizes;
  using type = typename TestFixture::type;

  using rng = distribution_selector<type>::type;

  std::mt19937 gen(12345);
  rng dis(get_min<type>(), get_max<type>());

  for (const size_t &size : sizes) {
    const size_t threads = std::min<size_t>(1024, size);
    const size_t blocks = CEIL_DIV(size, threads);

    std::vector<type> A(size), B(size), C(size);

    for (size_t i = 0; i < size; i++) {
      A[i] = dis(gen);
      B[i] = dis(gen);

      C[i] = A[i] + B[i];
    }

    type *d_a, *d_b, *d_out;
    HIP_CHECK(hipMalloc(&d_a, sizeof(type) * size));
    HIP_CHECK(hipMalloc(&d_b, sizeof(type) * size));
    HIP_CHECK(hipMalloc(&d_out, sizeof(type) * size));

    HIP_CHECK(
        hipMemcpy(d_a, A.data(), sizeof(type) * size, hipMemcpyHostToDevice));
    HIP_CHECK(
        hipMemcpy(d_b, B.data(), sizeof(type) * size, hipMemcpyHostToDevice));
    HIP_CHECK(hipDeviceSynchronize());

    vec_add<type><<<dim3(blocks), dim3(threads)>>>(d_a, d_b, d_out, size);

    HIP_CHECK(hipGetLastError());
    HIP_CHECK(hipDeviceSynchronize());

    std::vector<type> h_out(size);

    HIP_CHECK(hipMemcpy(h_out.data(), d_out, sizeof(type) * size,
                        hipMemcpyDeviceToHost));

    for (size_t i = 0; i < size; i++)
      EXPECT_EQ(C[i], h_out[i])
          << "Expected: " << C[i] << " Actual: " << h_out[i] << std::endl;

    HIP_CHECK(hipFree(d_a));
    HIP_CHECK(hipFree(d_b));
    HIP_CHECK(hipFree(d_out));
  }
}