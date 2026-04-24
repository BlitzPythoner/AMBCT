#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "write.h"

#define TEST_SIZE_MB 256
#define BUFFER_SIZE (4 * 1024 * 1024)

double write_test(const char* path, char* out_file) {
    snprintf(out_file, MAX_PATH, "%s\\ambct_test.bin", path);

    HANDLE file = CreateFileA(
        out_file,
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_FLAG_NO_BUFFERING | FILE_FLAG_SEQUENTIAL_SCAN,
        NULL
    );

    if (file == INVALID_HANDLE_VALUE) {
        return -1;
    }

    void* buffer = _aligned_malloc(BUFFER_SIZE, 4096);
    if (!buffer) return -1;

    memset(buffer, 0xAA, BUFFER_SIZE);

    DWORD written;
    unsigned long long total = 0;
    unsigned long long target = TEST_SIZE_MB * 1024ULL * 1024ULL;

    LARGE_INTEGER freq, start, end;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&start);

    while (total < target) {
        if (!WriteFile(file, buffer, BUFFER_SIZE, &written, NULL)) {
            break;
        }
        total += written;
    }

    FlushFileBuffers(file);

    QueryPerformanceCounter(&end);

    CloseHandle(file);
    _aligned_free(buffer);

    double seconds = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
    double mb = total / (1024.0 * 1024.0);

    return mb / seconds;
}