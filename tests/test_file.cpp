#include "src_file.h"
#include <assert.h>

void test_is_prime() {
    assert(is_prime(2) == true);
    assert(is_prime(3) == true);
    assert(is_prime(1) == false);
    assert(is_prime(4) == false);
    assert(is_prime(9) == false);
}

int main() {
    test_is_prime();
    return 0;
}
