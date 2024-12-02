// Michael Chen
// Advent of Code 2023 Day 6 part 1 and 2
// 12/13/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <cmath>
#include <ctime>
using namespace std;


int main () {

    clock_t timer = clock();
    string line;
    ifstream read_file;
    int p1 = 1, p2;
    vector<int> times;
    vector<int> dists;
    long long_time, long_dist;
    string temp_nums = "";

    read_file.open ("input");
    if (read_file.is_open()){
        //get times
        regex e ("[\\d]+");
        smatch num;
        getline(read_file, line);
        while(regex_search(line, num, e)){
            times.push_back(stoi(num.str(0)));
            temp_nums.append(num.str(0));
            line = num.suffix().str();
        }
        long_time = stol(temp_nums);

        temp_nums = "";
        // get distances
        getline(read_file, line);
        while(regex_search(line, num, e)){
            dists.push_back(stoi(num.str(0)));
            temp_nums.append(num.str(0));
            line = num.suffix().str();
        }
        long_dist = stol(temp_nums);
        read_file.close();
    }    

    for (int i=0; i<times.size(); i++){
        for (int a=0; a<times[i]; a++){
            if (a * (times[i] - a) > dists[i]){
                p1 *= (times[i] - 2*a + 1);
                break;
            }
        }
    }

    for (long a=int(sqrt(long_dist)); a>0; a--){
        if (a * (long_time - a) < long_dist){
            p2 = (long_time - 2*(a+1) + 1);
            break;
        }
    }

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 6 part 1: " << p1 << '\n';
    cout << "Day 6 part 2: " << p2 << '\n';

    return 0;
}