#include <iostream>

template <typename Iterator, typename Predicate>
Iterator mymax(
  Iterator first, Iterator last, Predicate pred){
    if (first == last) return nullptr;

    Iterator max_iter = first;
    first++;

    while (first != last) {
        if (pred(first, max_iter) == true) {
            max_iter = first;
        }
        first ++;
    }
    return max_iter;
}

template <typename Iterator> bool gt_int(Iterator first, Iterator second){
    return *first > *second;
}

int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };

int main(){
  const int* maxint = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int<const int*>);
  if (maxint == nullptr) {
    std::cout << "Array is empty!" << "\n";
    exit(0);
  }
  std::cout << *maxint << "\n";
}
