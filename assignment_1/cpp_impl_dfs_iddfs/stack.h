#ifndef STACK_H
#define STACK_H
#include "state.h"

class Stack {
private:
    int maxData;
    int numData;
    void** stack;
public:
/*************************************
 * Constructor
 * ***********************************/
    Stack();

/*************************************
 * Pushes data onto stack
 * ***********************************/
    void push(void*);

/*************************************
 * Pops data from stack. Returns the popped data
 * ***********************************/
    void* pop();

/*************************************
 * Decrements numData due to top of stack being NULL/already deleted
 * ***********************************/
    void fake_pop();

/*************************************
 * Returns the top of the stack without removing it from the stack
 * ***********************************/
    void* get_top();

/*************************************
 * Returns numData
 * ***********************************/
    int get_numData() {return numData;}

/*************************************
 * Returns true if the stack contains the given state
 * ***********************************/
    bool find(State*);

/*************************************
 * Returns true if the stack contains the given state, or if the given state is deeper than the one in the stack
 * ***********************************/
    bool find_iddfs(State*);

/*************************************
 * Destructor
 * ***********************************/
    ~Stack();

};

#endif
