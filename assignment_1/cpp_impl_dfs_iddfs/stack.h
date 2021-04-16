#ifndef STACK_H
#define STACK_H
#include "state.h"

class Stack {
private:
    int maxData;
    int numData;
    void** stack;
public:
    Stack();

    void push(void*);
    void* pop();

    void* get_top();
    bool find(State*);

    ~Stack();

    //~~~~~~~~~~~~~

    int get_numData() {return numData;}
};

#endif
