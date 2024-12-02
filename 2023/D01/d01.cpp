// Michael Chen
// Advent of Code Day 1 part 1 and 2
// 12/1/2023

#include <iostream>
#include <fstream>
#include <string>
#include <ctype.h>
using namespace std;

struct Trie{
    // lower case alphabet Trie
    int value;
    Trie* child[26];
    bool is_end;
};

Trie* trie_make(){
    // makes a trie
    Trie* root = (Trie*) calloc (1, sizeof(Trie));
    root->value = -1;
    root->is_end = false;
    for (int i; i <26; i++){
        root->child[i] = NULL;
    }
    return root;
}

void trie_insert(Trie* root, string text, int val){
    Trie* temp = root;
    for (const char& c : text){
        int i = c - 'a';
        if (temp->child[i] == NULL){
            Trie* new_node = trie_make();
            temp->child[i] = new_node;
            temp = new_node;
        } else {
            temp = temp->child[i];
        }
    }
    temp -> value = val;
    temp -> is_end = true;
}

int trie_search(Trie* root, string text){
    // Searches for word in the Trie
    Trie* temp = root;

    for(const char& c : text){
        int i = c - 'a';
        if (temp->child[i] == NULL)
            return temp->value;
        temp = temp->child[i];
    }
    if (temp != NULL && temp->is_end)
        return temp->value;
    return temp->value;
}

int first_last_numbers (string text, Trie* root, bool part2){
    // Finds the first and last numbers in `text` and splices them into a two
    // digit int.

    int first, last;
    bool start = true;
    Trie* temp = root;
    Trie* prev_root = NULL;
    int prev_i = 0; // no numbers start with a.

    for (const char& c : text){
        if (isdigit(c)){
            temp = root;
            if (start){
                first = c - '0';
                start = false;
            }
            last = c - '0';
        } 
        else if (part2){
            int i = c - 'a';
            prev_root = root->child[prev_i];
            temp = temp->child[i];
            if (temp == NULL){
                // case 1: node does not exist. 
                if (prev_root != NULL && prev_root->child[i] != NULL)
                    // case 1a: previous letter is a new start to number.
                    {temp = prev_root->child[i];}
                else if (root->child[i] != NULL) {temp = root->child[i];}
                    // case 1b: current letter is a new start to number.
                else {temp = root;}
                    // case 1c: need to restart number.
            }
            else if (temp->value > -1){
                if (start){
                    first = temp->value;
                    start = false;
                }
                last = temp->value;
                if (prev_root != NULL && prev_root->child[i] != NULL)
                 {temp = prev_root->child[i];}
                else if (root->child[i] != NULL) {temp = root->child[i];}
                else {temp = root;}
            }
            prev_i = i;
        }
    }

    return first * 10 + last;
}


int main () {

    string line;
    ifstream input;
    int sum_p1 = 0, sum_p2 = 0;

    Trie* number_trie = trie_make();
    trie_insert(number_trie, "zero", 0);
    trie_insert(number_trie, "one", 1);
    trie_insert(number_trie, "two", 2);
    trie_insert(number_trie, "three", 3);
    trie_insert(number_trie, "four", 4);
    trie_insert(number_trie, "five", 5);
    trie_insert(number_trie, "six", 6);
    trie_insert(number_trie, "seven", 7);
    trie_insert(number_trie, "eight", 8);
    trie_insert(number_trie, "nine", 9);

    input.open ("input");

    if (input.is_open()){
        while ( getline(input, line)){
            sum_p1 += first_last_numbers(line, number_trie, false);
            sum_p2 += first_last_numbers(line, number_trie, true);
        }
        cout << "Day 1 part 1: " << sum_p1 << '\n';
        cout << "Day 1 part 2: " << sum_p2 << '\n';

        input.close();
    }

    return 0;
}