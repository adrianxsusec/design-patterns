#include <iostream>

class CoolClass{
public:
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_;
};
class PlainOldClass{
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_;
};

int main() {
    std::cout << "Size of PlainOldClass: " << sizeof(PlainOldClass) << "\n";
    std::cout << "Size of CoolClass: " << sizeof(CoolClass) << "\n";
    // CoolClass has a pointer to VPTable (Virtual Pointer Table) - 4 for int, 8 for VPTable and 4 for padding
}