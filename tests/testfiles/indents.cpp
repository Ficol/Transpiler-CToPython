#include <iostream>


int main()
{
    int x;
    if(1 == 1)
    {
        if(2 == 2)
        {
            x = 2;
            while(x != 1)
            {
                std::cout << 3 << std::endl;
            }
            x = 3;
        }
        x = 1;
    }
    x = 0;
    return 0;
}
