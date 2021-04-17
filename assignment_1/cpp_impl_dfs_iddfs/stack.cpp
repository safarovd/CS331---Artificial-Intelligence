#include <iostream>
#include "stack.h"
#include "state.h"

using namespace std;

bool compare_states2(State* next, State* cur) {
    if (next->lchickens == cur->lchickens && next->lwolves == cur->lwolves && next->lboat == cur->lboat) {
        return true;
    }
    return false;
}

Stack::Stack() {
  numData = 0;
  maxData = 2;
  stack = new void*[maxData];
}

void Stack::push(void* data) {
  if (numData == maxData) {

    maxData *= 2;
    void** temp = new void*[maxData];
    

    for (int i = 0; i < numData; i++) {
      temp[i] = stack[i];
    }

    delete [] stack;
    stack = temp;
    
  }  
  stack[numData++] = data;
  

}

void* Stack::pop() {
  return stack[--numData];
}

void Stack::fake_pop() {
  numData--;
  return;
}

void* Stack::get_top() {
 return stack[numData - 1];
}

bool Stack::find(State* cur) {
  for (int i = 0; i < numData; i++) {
    if (compare_states2(cur, (State*)(stack[i]))) { 
      return true;
    }
  }
  return false;
}

bool Stack::find_iddfs(State* cur) {
  for (int i = 0; i < numData; i++) {
    if (compare_states2(cur, (State*)(stack[i])) && cur->depth >= ((State*)(stack[i]))->depth) { 
      return true;
    }
  }
  return false;
}

Stack::~Stack() {
  delete [] stack;
}