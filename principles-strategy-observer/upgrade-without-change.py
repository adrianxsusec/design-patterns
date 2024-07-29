def mymax(iterable, key=lambda x: x):
    max_x=max_key=None

    for x in iterable:
        if not max_x or key(x) > max_key:
            max_x = x
            max_key = key(x)

    return max_x

def string_list_test():
    string_list = ["aaa", "aac", "z", "aza", "zz"]
    string_key = lambda x: len(x)
    
    print(mymax(string_list, key=string_key))
    
def test_default_argument():
    max_int = mymax([1, 3, 5, 7, 4, 6, 9, 2, 0])
    max_char = mymax("Suncana strana ulice")
    max_string = mymax([
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"])
    
    print(f"Max int: {max_int}")
    print(f"Max char: {max_char}")
    print(f"Max string: {max_string}")
    
def test_dictionary():
    D={'burek':8, 'buhtla':5}
    max_val = mymax(D, D.get)
    print(f"Max val in dict: {max_val}") 
    
def test_tuples():
    tuples = [("name", "surname"), ("john", "doe"), ("ime", "prezime"), ("z", "z")]
    max_name = mymax(tuples)
    print(f"Max name is: {max_name}")

if __name__ == "__main__":
    test_tuples()