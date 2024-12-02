// Michael Chen
// Advent of Code 2023 Day 5 part 1 and 2
// 12/13/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <tuple>
#include <utility>
#include <ctype.h>
#include <ctime>
using namespace std;


vector<vector<long>> make_rules(vector<vector<long>> block){
    // Rules format: (range start inclusive, range end inclusive, offset)
    vector<vector<long>> rules;
    for (vector<long> line : block) {
        vector<long> temp;
        temp.push_back(line[1]);
        temp.push_back(line[1] + line[2] - 1);
        temp.push_back(line[0] - line[1]);
        rules.push_back(temp);
    }
    return rules;
}

void run_rules(vector<long> &ns, vector<vector<long>> rules){
    for (long &n: ns){
        for (const vector<long> rule : rules){
            if (n >= rule[0] && n <= rule[1]){
                n = n + rule[2];
                break;
            }
        }
    }
}

vector<pair<long,long>> run_pairs(vector<pair<long, long>> &ranges, vector<vector<long>> rules){

    vector<pair<long, long>> new_ranges;

    while (ranges.size() > 0){
        pair<long, long> cur_rng = ranges.back();
        ranges.pop_back();

        bool un_mapped = true;

        for (const vector<long> rule : rules){
            // iterate through all the rules.
            if (cur_rng.first < rule[0]){
                if (cur_rng.second < rule[0]){
                    // current range is entirely less than rule range
                    continue; // go to next rule
                } else if (cur_rng.second >= rule[0] && cur_rng.second <= rule[1]){
                    // current range intersects rule from below
                    ranges.push_back(make_pair(cur_rng.first, rule[0]-1)); // non-intersecting part of range
                    new_ranges.push_back(make_pair(rule[0] + rule[2], cur_rng.second + rule[2])); // intersecting part of range, + offset
                    un_mapped = false;
                    break; // go to next range
                } else if (cur_rng.second > rule[1]){
                    // current range encompasses rule range.
                    ranges.push_back(make_pair(cur_rng.first, rule[0]-1)); // non-intersecting part of range, below
                    ranges.push_back(make_pair(rule[1]+1, cur_rng.second)); // non-intersecting part of range, above
                    new_ranges.push_back(make_pair(rule[0]+rule[2], rule[1]+rule[2])); // applied offset to domain of rule
                    un_mapped = false;
                    break; 
                }
            } else if (cur_rng.first >= rule[0] && cur_rng.first <= rule[1]){
                if (cur_rng.second <= rule[1]){
                    // current range is entirely within rule range
                    new_ranges.push_back(make_pair(cur_rng.first+rule[2], cur_rng.second+rule[2]));
                    un_mapped = false;
                    break;
                } else if (cur_rng.second > rule[1]){
                    // current range intersects rule from above
                    ranges.push_back(make_pair(rule[1]+1, cur_rng.second));
                    new_ranges.push_back(make_pair(cur_rng.first+rule[2], rule[1]+rule[2]));
                    un_mapped = false;
                    break;
                }
            } else {
                // current range is entirely larger than rule range
                continue;
            }
        }
        if (un_mapped){new_ranges.push_back(cur_rng);} // if no rules applied to cur_rng, then no offset
    }
    return new_ranges;
}

int main () {

    clock_t timer = clock();
    string line;
    ifstream read_file;
    long sum_p1 = 0, sum_p2 = 0;
    vector<long> seeds;
    vector<vector<vector<long>>> rules_blocks;
    vector<vector<long>> block;
    vector<function<long(long)>> maps;

    read_file.open ("input");
    if (read_file.is_open()){
        //get seeds
        regex e ("[\\d]+");
        smatch num;
        getline(read_file, line);
        while(regex_search(line, num, e)){
            seeds.push_back(stol(num.str(0)));
            line = num.suffix().str();
        }

        bool push = false;
        while ( getline(read_file, line)){

            vector<long> map_line;
            if (isdigit(line[0])){ 
                push = true;
                while(regex_search(line, num, e)){
                    map_line.push_back(stol(num.str(0)));
                    line = num.suffix().str();
                }
                block.push_back(map_line);
            } else if (push) {
                push = false;
                rules_blocks.push_back(make_rules(block));
                block.clear();
            }
        }
        rules_blocks.push_back(make_rules(block));
        read_file.close();
    }

    vector<long> seeds_p1 = seeds;
    vector<pair<long, long>> seed_ranges_p2;

    for (int i =0; i < seeds.size(); i += 2){
        seed_ranges_p2.push_back(make_pair(seeds[i], seeds[i]+seeds[i+1]-1));
    }


    for (vector<vector<long>> rules: rules_blocks){
        run_rules(seeds_p1, rules);
        seed_ranges_p2 = run_pairs(seed_ranges_p2, rules);
    }

    long seeds_p2 = seed_ranges_p2.back().first;

    for (pair<long, long> &range : seed_ranges_p2){
        seeds_p2 = min(seeds_p2, range.first);
    }

    long p1 = *min_element(seeds_p1.begin(), seeds_p1.end());

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";

    cout << "Day 5 part 1: " << p1 << '\n';
    cout << "Day 5 part 2: " << seeds_p2 << '\n';
    return 0;
}