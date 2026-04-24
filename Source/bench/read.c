#include <windows.h>
#include <stdlib.h>
#include "read.h"

#define BUFFER_SIZE (4 * 1024 * 1024)

double read_test(const char* path) {
    HANDLE file = CreateFileA(
        path,
        GENERIC_READ,
        FILE_SHARE_READ,
        NULL,
        OPEN_EXISTING,
        FILE_FLAG_NO_BUFFERING | FILE_FLAG_SEQUENTIAL_SCAN,
        NULL
    );

    if (file == INVALID_HANDLE_VALUE) {
        return -1;
    }

    void* buffer = _aligned_malloc(BUFFER_SIZE, 4096);
    if (!buffer) return -1;

    DWORD read;
    unsigned long long total = 0;

    LARGE_INTEGER freq, start, end;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&start);

    while (ReadFile(file, buffer, BUFFER_SIZE, &read, NULL) && read > 0) {
        total += read;
    }

    QueryPerformanceCounter(&end);

    CloseHandle(file);
    _aligned_free(buffer);

    double seconds = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
    double mb = total / (1024.0 * 1024.0);

    return mb / seconds;
}