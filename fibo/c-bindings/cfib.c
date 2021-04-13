double cfibo(int n)
{
    int i;
    double a = 0, b = 1, tmp;
    for(i = 0; i < n; i++)
    {
        tmp = a;
        a += b;
        b = tmp;
    }
    return a;
}
