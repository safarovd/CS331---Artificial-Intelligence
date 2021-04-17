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

    void equals(State* cur) {
        lchickens = cur->lchickens;
        lwolves = cur->lwolves;
        lboat = cur->lboat;

        rchickens = cur->rchickens;
        rwolves = cur->rwolves;
        rboat = cur->rboat;

        prev = cur->prev;
        depth = cur->depth;
    }

    void print_state() {
    cout << "------------" << endl;
    cout << "C: " << lchickens << " || C: " << rchickens << endl;
    cout << "W: " << lwolves << " || W: " << rwolves << endl;
    cout << "B: " << lboat << " || B: " << rboat << endl;
    cout << "------------" << endl;

}

};

#endif