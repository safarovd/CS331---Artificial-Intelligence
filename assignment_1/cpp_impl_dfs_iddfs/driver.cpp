#include <iostream>
#include <fstream>
#include <string>
#include <cassert>
#include "stack.h"
#include "state.h"

using namespace std;

Stack* dfs(State*, State*);
bool is_goal(State*, State*);
void expand(Stack*, Stack*, State*);
bool game_over(State*);

//void iddfs(State, State);

void print_answer(Stack*, char*);
void print_state(State*);
void print_state_file(State*, ofstream &);
void state_equals_state(State*, State*);
bool compare_states(State*, State*);

int totalExpanded = 0;
//Command line arguments: <initial State file> <goal State file> <mode> <output file>
int main(int argc, char** argv) {

    State* s = new State;
    ifstream input(argv[1]);
    string temp;
    getline(input, temp, ',');
    s->lchickens = stoi(temp);
    getline(input, temp, ',');
    s->lwolves = stoi(temp);
    getline(input, temp);
    s->lboat = stoi(temp);
    getline(input, temp, ',');
    s->rchickens = stoi(temp);
    getline(input, temp, ',');
    s->rwolves = stoi(temp);
    getline(input, temp);
    s->rboat = stoi(temp);
    input.close();
    s->prev = NULL;
    s->depth = 0;

    State* g = new State;
    input.open(argv[2]);
    getline(input, temp, ',');
    g->lchickens = stoi(temp);
    getline(input, temp, ',');
    g->lwolves = stoi(temp);
    getline(input, temp);
    g->lboat = stoi(temp);
    getline(input, temp, ',');
    g->rchickens = stoi(temp);
    getline(input, temp, ',');
    g->rwolves = stoi(temp);
    getline(input, temp);
    g->rboat = stoi(temp);
    input.close();

    Stack* answer;
    if (argv[3][0] == 'D' || argv[3][0] == 'd') {    //dfs
        cout << "------------DFS Traversal------------" << endl;
        answer = dfs(s, g);

    }
    else {                      //iddfs
        cout << "------------IDDFS Traversal------------" << endl;
        //Stack answer = iddfs(s, g);

    }
    print_answer(answer, argv[4]);

    delete s;
    delete g;

    return 0;
}

Stack* dfs(State* cur, State* g) {
    Stack* frontier = new Stack;
    Stack* explored = new Stack;
    frontier->push(cur);
    totalExpanded++;
    expand(frontier, explored, cur);
    
    while (true) {
        if (!(frontier->get_numData())) {
            return frontier;
        }
        cur = (State*)(frontier->pop());
        explored->push(cur);

        if (is_goal(g, cur)) {
            return explored;
        }

        if (!(game_over(cur))) {
            totalExpanded++;
            expand(frontier, explored, cur);
        }

    }
}

void expand(Stack* frontier, Stack* explored, State* cur) {
    
    if (cur->lboat) {
        
        if (cur->lchickens > 0) {                    //put one chicken in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->lchickens -= 1;
            next->rchickens += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }
        if (cur->lchickens > 1) {                    //put 2 chickens in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->lchickens -= 2;
            next->rchickens += 2;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 0) {                      //put 1 wolf in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->lwolves -= 1;
            next->rwolves += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 0 && cur->lchickens > 0) { //put 1 wolf and 1 chicken in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->lwolves -= 1;
            next->rwolves += 1;
            next->lchickens -= 1;
            next->rchickens += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 1) {                      //put 2 wolves in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->lwolves -= 2;
            next->rwolves += 2;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }

    }
    else {
        if (cur->rchickens > 0) {                    //put one chicken in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->rchickens -= 1;
            next->lchickens += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;
            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }

        if (cur->rchickens > 1) {                    //put 2 chickens in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->rchickens -= 2;
            next->lchickens += 2;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }

        if (cur->rwolves > 0) {                      //put 1 wolf in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->rwolves -= 1;
            next->lwolves += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        
        if (cur->rwolves > 0 && cur->rchickens > 0) { //put 1 wolf and 1 chicken in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->rwolves -= 1;
            next->lwolves += 1;
            next->rchickens -= 1;
            next->lchickens += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }

        if (cur->rwolves > 1) {                      //put 2 wolves in the boat
            State* next = new State;
            state_equals_state(next, cur);
            next->rwolves -= 2;
            next->lwolves += 2;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(frontier->find(next) || explored->find(next))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
    }
}

bool is_goal(State* g, State* cur) {
    if (compare_states(g, cur)) {
        return true;
    }
    return false;
}

bool game_over(State* cur) {
    if (cur->lwolves > cur->lchickens && cur->lchickens > 0) {
        return true;
    }
    if (cur->rwolves > cur->rchickens && cur->rchickens > 0) {
        return true;
    }
    return false;
}

void print_state(State* cur) {
    cout << "------------" << endl;
    cout << "C: " << cur->lchickens << " || C: " << cur->rchickens << endl;
    cout << "W: " << cur->lwolves << " || W: " << cur->rwolves << endl;
    cout << "B: " << cur->lboat << " || B: " << cur->rboat << endl;
    cout << "------------" << endl;

}

void print_state_file(State* cur, ofstream &file) {
    file << "------------" << endl;
    file << "C: " << cur->lchickens << " || C: " << cur->rchickens << endl;
    file << "W: " << cur->lwolves << " || W: " << cur->rwolves << endl;
    file << "B: " << cur->lboat << " || B: " << cur->rboat << endl;
    file << "------------" << endl;

}

void print_answer(Stack* answer, char* file) {
    
    State* cur = (State*)(answer->get_top());
    Stack* fout = new Stack;

    for (int i = cur->depth; i >= 0; i--) {
        
        print_state(cur);
        fout->push(cur);
        cur = cur->prev;
        
    }

    ofstream in(file);
    for(int i = fout->get_numData(); i > 0 ; i--) {

        print_state_file((State*)(fout->pop()), in);

    }
    in.close();

    cout << "This is the initial state. Scrolling up progresses through the actions." << endl;
    cout << "EXPANDED NODES: " << totalExpanded << endl;
    cout << "PATH SIZE: " << ((State*)(answer->get_top()))->depth << endl;
}

void state_equals_state(State* next, State* cur) {
        next->lchickens = cur->lchickens;
        next->lwolves = cur->lwolves;
        next->lboat = cur->lboat;

        next->rchickens = cur->rchickens;
        next->rwolves = cur->rwolves;
        next->rboat = cur->rboat;
}

bool compare_states(State* next, State* cur) {
    if (next->lchickens == cur->lchickens && next->lwolves == cur->lwolves && next->lboat == cur->lboat) {
        return true;
    }
    return false;
}