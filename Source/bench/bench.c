#include <stdio.h>
#include <windows.h>

#include "read.h"
#include "write.h"

#define VERSION "v1.0"
#define AUTHOR  "BlitzPythoner"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: bench.exe <source_path> <target_path>\n");
        return 1;
    }

    const char* source = argv[1];
    const char* target = argv[2];

    printf("AMBCT Disk Benchmark Tool %s by %s\n\n", VERSION, AUTHOR);

    char write_file[MAX_PATH];
    char read_file[MAX_PATH];

    double write_speed = write_test(target, write_file);
    if (write_speed < 0) {
        printf("Write test failed.\n");
        return 1;
    }

    double prep = write_test(source, read_file);
    if (prep < 0) {
        printf("Failed to prepare read test file.\n");
        DeleteFileA(write_file);
        return 1;
    }

    double read_speed = read_test(read_file);
    if (read_speed < 0) {
        printf("Read test failed.\n");
        DeleteFileA(write_file);
        DeleteFileA(read_file);
        return 1;
    }

    DeleteFileA(write_file);
    DeleteFileA(read_file);

    printf("Read: %.1f MB/s, Write: %.1f MB/s \n",
           read_speed, write_speed);

    return 0;
}