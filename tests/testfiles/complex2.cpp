#include <iostream>


int main()
{
    int x;
    x = 5;
    while(x > 0)
    {
        if(x % 3 == 0)
        {
            std::cout << 0 << std::endl;
        }
        if(x % 3 == 1)
        {
            std::cout << 1 << std::endl;
        }
        else
        {
            std::cout << 2 << std::endl;
        }
        x = x - 1;
    }
    return 0;
}
