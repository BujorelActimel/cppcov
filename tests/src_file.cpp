#include "src_file.h"
#include "module.h"

bool is_prime(int num) {
    if (num < 2) {
        return false;
    }
    if (num == 2) {
        return true;
    }
    if (is_div(num, 2)) {
        return false;
    }
    for (int div = 3; div * div <= num; div += 2) {
        if (is_div(num, div)) {
            return false;
        }
    }
    return true;
}