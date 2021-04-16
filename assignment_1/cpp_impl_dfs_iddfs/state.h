#ifndef STATE_H
#define STATE_H
#include <iostream>

using namespace std;

class State {
public:
    int lchickens;
    int lwolves;
    bool lboat;

    int rchickens;
    int rwolves;
    bool rboat;

    State* prev;
    int depth;

};

#endif