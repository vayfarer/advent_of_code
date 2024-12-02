// Michael Chen
// Advent of Code 2023 Day 4 part 1 and 2
// 12/4/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <unordered_set>
using namespace std;

int main () {

    string line;
    ifstream read_file;
    int sum_p1 = 0, sum_p2 = 0;
    vector<int> scores;

    regex e ("[\\d]+");

    read_file.open ("input");

    if (read_file.is_open()){
        while ( getline(read_file, line)){
            int sep = line.find_first_of('|');
            int col = line.find_first_of(':') + 1;
            string win_str = line.substr(col, sep-col);
            string scr_str = line.substr(sep, string::npos);

            smatch nums;
            unordered_set<int> win_nums;

            while(regex_search(win_str, nums, e)){
                win_nums.insert(stoi(nums.str(0)));
                win_str = nums.suffix().str();
            }

            int copies = 0;
            int exp = 0;
            while(regex_search(scr_str, nums, e)){
                if (win_nums.count(stoi(nums.str(0)))){
                    copies ++;
                    if (exp == 0){
                        exp ++;
                    } else {
                        exp *= 2;
                    }
                }
                scr_str = nums.suffix().str();
            }
            scores.push_back(copies);
            sum_p1 += exp;
        }
        read_file.close();
    }

    for (int i = scores.size()-1; i >= 0; i--){
        size_t forward = scores[i];
        scores[i] = 1;
        for (int j = i + 1; j <= min(scores.size()-1, i+forward); j++){
            scores[i] += scores[j];
        }
        sum_p2 += scores[i];
    }

    std::cout << "Day 4 part 1: " << sum_p1 << '\n';
    std::cout << "Day 4 part 2: " << sum_p2 << '\n';
    return 0;
}
