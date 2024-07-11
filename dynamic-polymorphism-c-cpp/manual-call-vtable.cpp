#include <iostream>

class B{
public:
  virtual int prva()=0;
  virtual int druga(int)=0;
};

class D: public B{
public:
  virtual int prva(){return 42;}
  virtual int druga(int x){return prva()+x;}
};


void print_methods(B* pb) {
  
  typedef int(*FirstFunc)(B*);
  typedef int(*SecondFunc)(B*, int);

  void*** vtable_address = (void***)pb;
  void** vtable = *vtable_address;

  FirstFunc first = (FirstFunc)vtable[0];
  SecondFunc second = (SecondFunc)vtable[1];

  int first_res = first(pb);
  int second_res = second(pb, 5);

  std::cout << "prva() = " << first_res << std::endl;
  std::cout << "druga(5) = " << second_res << std::endl;
}

int main() {
    D obj;
    print_methods(&obj);
}