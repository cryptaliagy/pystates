from pystates import stateful, use_state

@stateful
def counter():
    count, set_count = use_state(0)
    set_count(count + 1)  # Set the next state
    return count

@stateful
def fibbonaci():
    first, set_first = use_state(0)
    second, set_second = use_state(1)
    nxt = first + second
    set_first(second)
    set_second(nxt)
    return first

if __name__ == "__main__":
    print('Testing Stateful decorator!')
    for i in range(10):
        print(counter())
    
    print('Fibbonaci series (displaying 2 saved states):')
    for i in range(10):
        print(fibbonaci())