// Michael Chen
// Advent of Code 2023 Day 9 part 1 and 2
// 12/31/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <ctime>
#include <cctype>
using namespace std;

pair<int, int> diff_step(vector <int> nums){
    vector <int> diffs;
    bool zeroes = true;
    for (int i = 0; i < nums.size() - 1; i++){
        int new_diff = nums[i+1] - nums[i];
        diffs.push_back(new_diff);
        if (new_diff) {zeroes = false;}
    }
    if (zeroes){
        return make_pair(nums.front(), nums.back());
    }
    pair<int, int> next_diff = diff_step(diffs);
    next_diff.first = nums.front() - next_diff.first;
    next_diff.second += nums.back();
    return next_diff;
}

int main () {

    clock_t timer = clock();

    string line;
    ifstream read_file;
    long p1 = 0, p2 = 0;

    read_file.open ("input");
    if (read_file.is_open()){

        regex e ("(-?[\\d]+)");
        smatch nums;

        while(getline(read_file, line)){
            vector <int> num_line;
            while(regex_search(line, nums, e)){
                num_line.push_back(stoi(nums.str(0)));
                line = nums.suffix().str();
            }

            pair<int, int> next_steps = diff_step(num_line);
            p1 += next_steps.second;
            p2 += next_steps.first;
        }
        read_file.close();
    }    

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 9 part 1: " << p1 << '\n';
    cout << "Day 9 part 2: " << p2 << '\n';

    return 0;
}