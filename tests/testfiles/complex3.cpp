#include <iostream>

int factorial(int n)
{
    if(! n)
    {
        return 1;
    }
    m = n - 1;
    return factorial(m);
}

int main()
{
    int x;
    int i;
    float z;
    float z;
    factorial(5);
    x = factorial(10);
    std::cout << x << factorial(7) << std::endl;
    i = 0;
    while(i < 100)
    {
        if(i % 7 == 0)
        {
            z = factorial(i);
            z = z * z;
        }
        else
        {
            z = factorial(i);
            z = z * z * z;
        }
    }
    x = 2;
    std::cout << std::endl;
    return 0;
}
