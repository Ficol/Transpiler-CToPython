#include <iostream>

int sum(int a, int b)
{
    return a + b;
}

int main()
{
    float x;
    int y;
    x = 2.4;
    while(x > 0 && 1 == 1)
    {
        x = x - 1;
        std::cout << x << std::endl;
    }
    y = 3 + 2 * 2;
    std::cout << sum(x, y) << 2 << std::endl;
    return 0;
}
