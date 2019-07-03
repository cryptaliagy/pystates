from functools import wraps
from inspect import currentframe

def singleclosure(func):
    return func()


class Node:
    def __init__(self, val, next):
        self.val = val
        self.next = next
    def __repr__(self):
        return 'Node(%s, %s)' % (self.val, self.next)


def stateful(func):
    '''Decorator to allow functions to be stateful'''

    head = Node(None, None)
    head.curr = head

    def set_state(node):
        def set_(new):
            node.val = new
        return set_

    def get_state(default):
        if head.curr.next == None:
            nxt = Node(default, None)
            head.curr.next = nxt
        head.curr = head.curr.next
        return (head.curr.val, set_state(head.curr))
    
    use_state.states[func.__name__] = get_state  # Adds this function's state getter to the use_states state dictionary

    @wraps(func)
    def wrapper(*args, **kwargs):
        returned = func(*args, **kwargs)
        head.curr = head # Restart the state queue after all states have been called or defined
        return returned # Return the result of the function
    return wrapper


@singleclosure
def use_state():
    def use_state(default):
        caller = currentframe().f_back.f_code.co_name
        if caller not in use_state.states:
            raise RuntimeError('Can only use use_state inside stateful functions! Did you forget the stateful decorator?')
        return use_state.states[caller](default)
    use_state.states = {} # Creates the 'global' state queue as a closure of this function

    return use_state