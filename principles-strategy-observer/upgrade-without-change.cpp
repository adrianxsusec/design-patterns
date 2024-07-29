#include <iostream>

template <typename Iterator, typename Predicate>
Iterator mymax(
  Iterator first, Iterator last, Predicate pred){
    if (first == last) return last;

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

template <typename T> bool gt_int(T first, T second){
    return *first > *second;
}

template <typename T> bool gt_str(T first, T second){
    return strcmp(*first, *second) > 0;
}

void test_int_array() {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    const int* max_int = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int<const int*>);
    if (max_int == nullptr) {
        std::cout << "Array is empty!" << "\n";
        exit(0);
    }
    std::cout << *max_int << "\n";
}

void test_string_array() {
    const char* arr_str[] = {"First", "second", "third", "zz"};
    const char** max_str = mymax(arr_str, arr_str + sizeof(arr_str)/sizeof(arr_str[0]), gt_str<const char**>);
    if (max_str == nullptr) {
        std::cout << "Array is empty!" << "\n";
        exit(0);
    }
    std::cout << *max_str << "\n";
}

void test_vector() {
    std::vector<int> v = {1, 5, 19, 2};
    auto max_iter = mymax(v.begin(), v.end(), gt_int<std::vector<int>::iterator>);
    if (max_iter != v.end()) {
        std::cout << "Max value in vector: " << *max_iter << "\n";
    } else {
        std::cout << "Vector is empty!" << "\n";
    }
}

int main(){
    test_int_array();
    test_string_array();
    test_vector();
    return 0;
}
