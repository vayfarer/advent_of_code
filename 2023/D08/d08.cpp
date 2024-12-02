// Michael Chen
// Advent of Code 2023 Day 8 part 1 and 2
// 12/25/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <cmath>
#include <numeric>
#include <map>
#include <ctime>
#include <cctype>
using namespace std;


int main () {

    clock_t timer = clock();

    string line;
    string instructions;
    ifstream read_file;
    int p1 = 0;
    long p2 = 1;
    unordered_map <string, pair<string, string>> node_map;
    vector <string> start_nodes_p2;

    read_file.open ("input");
    if (read_file.is_open()){

        getline(read_file, instructions); // instructions line
        getline(read_file, line); // blank line
        
        regex e ("(\\w+) = \\((\\w+), (\\w+)\\)");
        smatch node;
        while(getline(read_file, line)){
            regex_match(line, node, e);
            node_map.emplace(node.str(1), make_pair(node.str(2), node.str(3)));
            if (node.str(1)[2] == 'A'){
                start_nodes_p2.push_back(node.str(1));
            }
        }
        read_file.close();
    }    

    string node = "AAA";
    while (node != "ZZZ") {
        char &move = instructions[p1 % instructions.size()];
        node = (move == 'R') ? node_map.at(node).second : node_map.at(node).first;
        p1++;
    }

    vector <int> moves_p2;
    for (string &node_p2: start_nodes_p2){
        int n = 0;
        while (node_p2[2] != 'Z') {
            char &move = instructions[n % instructions.size()];
            node_p2 = (move == 'R') ? node_map.at(node_p2).second : node_map.at(node_p2).first;
            n++;
        }
        moves_p2.push_back(n);
    }

    for (int &n: moves_p2){
        p2 = lcm(p2, n);
    }

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 8 part 1: " << p1 << '\n';
    cout << "Day 8 part 2: " << p2 << '\n';

    return 0;
}