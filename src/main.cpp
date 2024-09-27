#include "facedetectcnn.h"
#include <cstdio>
#include <cstring>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <vector>
namespace py = pybind11;

#define DETECT_BUFFER_SIZE 0x9000

std::vector<std::tuple<int, int, int, int, int>>
detectRGB(int width, int height, const char *input_ptr) {
  unsigned char *pBuffer = (unsigned char *)malloc(DETECT_BUFFER_SIZE);
  if (!pBuffer) {
    throw std::runtime_error("Can not alloc detect buffer.");
  }

  int imageBufferSize = width * height * 3;
  unsigned char *imageBuffer =
      (unsigned char *)malloc(imageBufferSize * sizeof(unsigned char));
  if (!pBuffer) {
    throw std::runtime_error("Can not alloc image buffer.");
  }
  memcpy(imageBuffer, input_ptr, imageBufferSize * sizeof(unsigned char));
  for (int idx = 0; idx < imageBufferSize; idx += 3) {
    unsigned char r = imageBuffer[idx];
    unsigned char b = imageBuffer[idx + 2];
    imageBuffer[idx] = b;
    imageBuffer[idx + 2] = r;
  }

  int *pResults = nullptr;
  pResults = facedetect_cnn(pBuffer, imageBuffer, width, height, width * 3);

  std::vector<std::tuple<int, int, int, int, int>> output;
  int num_result = pResults ? pResults[0] : 0;
  for (int i = 0; i < num_result; ++i) {
    short *p = ((short *)(pResults + 1)) + 16 * i;
    int confidence = p[0];
    int x = p[1];
    int y = p[2];
    int w = p[3];
    int h = p[4];
    output.push_back(std::make_tuple(x, y, w, h, confidence));
  }
  return output;
}

PYBIND11_MODULE(slimeface, m) {
  m.doc() =
      "A tiny and fast face detector with no numpy dependency"; // optional
                                                                // module
                                                                // docstring
  m.def("detectRGB", &detectRGB, "detection function requires RGB bytes");
}
