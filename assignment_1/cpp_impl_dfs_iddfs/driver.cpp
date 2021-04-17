#include <iostream>
#include <fstream>
#include <string>
#include <cassert>
#include "stack.h"
#include "state.h"

using namespace std;

void dfs(State*, State*, Stack*, Stack*);
void iddfs(State*, State*, Stack*, Stack*);

bool is_goal(State*, State*);
void expand(Stack*, Stack*, State*, int);
bool game_over(State*);

void print_answer(Stack*, char*);
bool already_have_node(Stack*, Stack*, State*, int);

void delete_stack(Stack*);

int totalExpanded = 0;

//Command line arguments: <initial State file> <goal State file> <mode> <output file>
int main(int argc, char** argv) {

/*************************************
 * data gathering
 * /
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
/*
 * data gathering
 *************************************/

    Stack* frontier = new Stack;
    Stack* explored = new Stack;

    if (argv[3][0] == 'D' || argv[3][0] == 'd') {
        cout << "------------DFS Traversal------------" << endl;
        dfs(s, g, frontier, explored);                                //DFS

    }
    else {                      //iddfs
        cout << "------------IDDFS Traversal------------" << endl;
        iddfs(s, g, frontier, explored);                               //IDDFS

    }

    print_answer(explored, argv[4]);
    delete_stack(explored);
    delete_stack(frontier);

    delete s;
    delete g;

    return 0;
}

/*************************************
 * Finds the a solution using dfs
 * ***********************************/
void dfs(State* s, State* g, Stack* frontier, Stack* explored) {
    State* cur = new State;
    cur->equals(s);
    frontier->push(cur);
    totalExpanded++;
    expand(frontier, explored, cur, 1);
    
    while (true) {

        if (!(frontier->get_numData())) {
            return;
        }

        cur = (State*)(frontier->pop());                    //explore a node
        explored->push(cur);

        if (is_goal(g, cur)) {                              //is the current node a goal state?
            return;
        }

        if (!(game_over(cur))) {                            //if the current node is not a terminal state, expand it
            totalExpanded++;
            expand(frontier, explored, cur, 1);
        }
    }
}

/*************************************
 * Finds the a solution using iddfs
 * ***********************************/
void iddfs(State* s, State* g, Stack* frontier, Stack* explored) {
    State* cur = new State;
    cur->equals(s);
    frontier->push(cur);
    totalExpanded++;
    expand(frontier, explored, cur, 2);
    int l = 1;                                              //initialize max depth to 1
    
    while (true) {
        if (!(frontier->get_numData())) {
            return;
        }

        cur = (State*)(frontier->pop());                    //explore a node
        explored->push(cur);

        if (is_goal(g, cur)) {                              //is the current node a goal state?
            return;
        }

        if (!(game_over(cur)) && cur->depth < l) {          //if the current node is not a terminal state, expand it
            totalExpanded++;
            expand(frontier, explored, cur, 2);
        }

        if (!(frontier->get_numData())) {
            l++;
            for (int i = explored->get_numData(); i > 0; i--) {
                delete (State*)(explored->pop());
            }
            cur = new State;
            cur->equals(s);
            frontier->push(cur);
            totalExpanded++;
            expand(frontier, explored, cur, 2);

        }
    }
}

/*************************************
 * Finds all possible states that are 1 action away from current state. Pushes them onto the frontier.
 * ***********************************/
void expand(Stack* frontier, Stack* explored, State* cur, int alg) {
    
    if (cur->lboat) {                                //is the boat on the left?
        
        if (cur->lchickens > 0) {                    //put one chicken in the boat
            State* next = new State;
            next->equals(cur);
            next->lchickens -= 1;
            next->rchickens += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }
        if (cur->lchickens > 1) {                    //put 2 chickens in the boat
            State* next = new State;
            next->equals(cur);
            next->lchickens -= 2;
            next->rchickens += 2;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 0) {                      //put 1 wolf in the boat
            State* next = new State;
            next->equals(cur);
            next->lwolves -= 1;
            next->rwolves += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 0 && cur->lchickens > 0) { //put 1 wolf and 1 chicken in the boat
            State* next = new State;
            next->equals(cur);
            next->lwolves -= 1;
            next->rwolves += 1;
            next->lchickens -= 1;
            next->rchickens += 1;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        if (cur->lwolves > 1) {                      //put 2 wolves in the boat
            State* next = new State;
            next->equals(cur);
            next->lwolves -= 2;
            next->rwolves += 2;
            next->lboat = false;
            next->rboat = true;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }

    }
    else {                                           //boat is on the right side
        if (cur->rchickens > 0) {                    //put one chicken in the boat
            State* next = new State;
            next->equals(cur);
            next->rchickens -= 1;
            next->lchickens += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }
        }

        if (cur->rchickens > 1) {                    //put 2 chickens in the boat
            State* next = new State;
            next->equals(cur);
            next->rchickens -= 2;
            next->lchickens += 2;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }

        if (cur->rwolves > 0) {                      //put 1 wolf in the boat
            State* next = new State;
            next->equals(cur);
            next->rwolves -= 1;
            next->lwolves += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
        
        if (cur->rwolves > 0 && cur->rchickens > 0) { //put 1 wolf and 1 chicken in the boat
            State* next = new State;
            next->equals(cur);
            next->rwolves -= 1;
            next->lwolves += 1;
            next->rchickens -= 1;
            next->lchickens += 1;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }

        if (cur->rwolves > 1) {                      //put 2 wolves in the boat
            State* next = new State;
            next->equals(cur);
            next->rwolves -= 2;
            next->lwolves += 2;
            next->lboat = true;
            next->rboat = false;
            next->prev = cur;
            next->depth = cur->depth + 1;

            if (!(already_have_node(frontier, explored, next, alg))) {
                frontier->push(next);
            }
            else {
                delete next;
            }

        }
    }
}

/*************************************
 * Returns true if the given node already exists in the explored or frontier.
 * IDDFS returns will return false if the already existing node is deeper than the given one.
 * ***********************************/
bool already_have_node(Stack* frontier, Stack* explored, State* cur, int alg) {
    if (alg == 1) {
        if (frontier->find(cur) || explored->find(cur)) {
            return true;
        }
        return false;
    }
    if (frontier->find_iddfs(cur) || explored->find_iddfs(cur)) {
        return true;
    }
    return false;

}

/*************************************
 * Returns true if the given state is a goal state
 * ***********************************/
bool is_goal(State* g, State* cur) {
    if (g->compare_states(cur)) {
        return true;
    }
    return false;
}

/*************************************
 * Returns true if the given state is a terminal/game over state
 * ***********************************/
bool game_over(State* cur) {
    if (cur->lwolves > cur->lchickens && cur->lchickens > 0) {
        return true;
    }
    if (cur->rwolves > cur->rchickens && cur->rchickens > 0) {
        return true;
    }
    return false;
}

/*************************************
 * Prints the path to the goal state both to the terminal and to the file specified by the user
 * ***********************************/
void print_answer(Stack* explored, char* file) {
    
    State* cur = (State*)(explored->get_top());
    Stack* answer = new Stack;

    for (int i = cur->depth; i >= 0; i--) {
        
        cur->print_state();
        answer->push(cur);
        cur = cur->prev;
        
    }

    ofstream in(file);
    for(int i = answer->get_numData(); i > 0 ; i--) {
        cur = (State*)(answer->pop());
        cur->print_state_file(in);

    }
    in.close();
    delete_stack(answer);

    cout << "This is the initial state. Scrolling up progresses through the actions." << endl;
    cout << "EXPANDED NODES: " << totalExpanded << endl;
    cout << "PATH SIZE: " << ((State*)(explored->get_top()))->depth << endl;
}

/*************************************
 * Deletes a stack object
 * ***********************************/
void delete_stack(Stack* stack) {
    for (int i = stack->get_numData(); i > 0; i--) {
        if ((State*)(stack->get_top()) == NULL) {
            stack->fake_pop();
        }
        else {
                delete (State*)(stack->pop());
        }
    }
    delete stack;
}