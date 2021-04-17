#ifndef STATE_H
#define STATE_H
#include <iostream>
#include <fstream>

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

    bool compare_states(State* other) {
        if (lchickens == other->lchickens && lwolves == other->lwolves && lboat == other->lboat) {
            return true;
        }
        return false;
    }

    void print_state() {
        cout << "------------" << endl;
        cout << "C: " << lchickens << " || C: " << rchickens << endl;
        cout << "W: " << lwolves << " || W: " << rwolves << endl;
        cout << "B: " << lboat << " || B: " << rboat << endl;
        cout << "------------" << endl;

    }

    void print_state_file(ofstream &file) {
        file << "------------" << endl;
        file << "C: " << lchickens << " || C: " << rchickens << endl;
        file << "W: " << lwolves << " || W: " << rwolves << endl;
        file << "B: " << lboat << " || B: " << rboat << endl;
        file << "------------" << endl;

    }

};

#endif