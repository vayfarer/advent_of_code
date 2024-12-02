// Michael Chen
// Advent of Code 2023 Day 10 part 1 and 2
// 1/1/2024

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <ctime>
#include <cctype>
#include <unordered_map>
#include <unordered_set>
using namespace std;

int main () {
    clock_t timer = clock();
    string line;
    ifstream read_file;
    int p1 = 0, p2 = 0;
    vector <string> pipes;
    pair <int, int> start;

    read_file.open ("input");
    if (read_file.is_open()){

        regex e ("(S)");
        smatch sm;
        int n = 0;
        
        while(getline(read_file, line)){
            pipes.push_back(line);
            if (regex_search(line, sm, e)){
                start.first = n;
                start.second = sm.position(0);
            }
            n++;
        }
        read_file.close();
    }    

    pair <int, int> down = make_pair(1,0), right = make_pair(0,1), up = make_pair(-1,0), left = make_pair(0,-1);

    unordered_map <string, pair<int, int>> step_offsets = {
        {"down", down},
        {"right", right},
        {"up", up},
        {"left", left}
    };

    unordered_map <string, unordered_set<char>> around = {
        {"down",{'J','L','|'}},//down
        {"right",{'J','-','7'}},//right
        {"up",{'|','F','7'}},//up
        {"left",{'-','F','L'}}//left
    };

    unordered_map <char, unordered_map<string, string>> pipe_routes = {
        {'J',{{"down", "left"},{"right", "up"}}},
        {'L',{{"down", "right"},{"left", "up"}}},
        {'|',{{"down", "down"},{"up", "up"}}},
        {'-',{{"left", "left"},{"right", "right"}}},
        {'7',{{"right", "down"},{"up", "left"}}},
        {'F',{{"left", "down"},{"up", "right"}}},
    };

    unordered_map <string, string> reverse = {
        {"left", "right"},
        {"right", "left"},
        {"up", "down"},
        {"down", "up"}
    };

    string next_step;
    pair <int, int> position = start;
    pair <string, string> start_pipe;
    char* next_pipe;

    //find start direction
    for (auto direction: around){
        pair <int, int> step = make_pair(start.first + step_offsets[direction.first].first, start.second + step_offsets[direction.first].second);
        if (step.first >= 0 && step.first < pipes.size() && step.second >=0 && step.second < pipes[0].size()){
            if (direction.second.count(pipes[step.first][step.second])){
                // valid step
                next_step = direction.first;
                start_pipe.first = reverse[next_step];
                next_pipe = &pipes[step.first][step.second];
                break;
            }
        }
    }

    // traverse pipe loop
    unordered_set <char*> pipe_loop;
    while (*next_pipe !='S'){
        pipe_loop.emplace(next_pipe);
        position.first += step_offsets[next_step].first;
        position.second += step_offsets[next_step].second;     
        next_pipe = &pipes[position.first][position.second];    
        start_pipe.second = next_step; // last pipe direction before hitting start. 
        next_step = pipe_routes[*next_pipe][next_step];    
    }
    pipe_loop.emplace(next_pipe);
    p1 = pipe_loop.size()/2;
    
    // replace start pipe
    for (auto pipe: pipe_routes){
        if (pipe.second.count(start_pipe.first) && pipe.second.count(start_pipe.second)){
            pipes[start.first][start.second] = pipe.first;
        }
    }

    unordered_map <char, char> pipe_joints = {{'F','J'},{'L','7'}};

    // iterate all positions not in pipe loop
    for (string &s: pipes){
        for (int i = 0; i < s.size(); i++){
            if (!pipe_loop.count(&s[i])){
                int m = 0;
                int j = i;
        
                while (j < s.size()){
                    if (pipe_loop.count(&s[j])){
                        // count pipe crossings to edge. Odd crossings means inside the loop.
                        if (s[j] == '|'){
                            m++;
                        }                    
                        else if (pipe_joints.count(s[j])) {
                            // F--J or L----7 are considered one pipe crossing. 
                            char cross_joint = pipe_joints[s[j]];
                            j++;
                            while (j < s.size() && s[j] == '-'){
                                j++;
                            }
                            if (s[j] == cross_joint){
                                m++;
                            }
                        }
                    } 
                    j++;
                }
                if (m % 2){
                    p2++;
                }

            }
        }
    }


    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 10 part 1: " << p1 << '\n';
    cout << "Day 10 part 2: " << p2 << '\n';

    return 0;
}