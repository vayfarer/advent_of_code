// Michael Chen
// Advent of Code 2023 Day 3 part 1 and 2
// 12/3/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
using namespace std;

bool adjacent_symb(int row, int beg, int len, vector<string> &in_data){
    // check if numbers have adjacent symbols
    // row: row of number in_data; beg: start index of number; len: length of number substr.

    // set search space in row
    if (beg > 0){beg--; len ++;}
    if (beg + len < in_data[0].length()){len++;}

    regex e("[^.\\d]");
    smatch m;

    // check rows, if it exists
    for (int i = -1; i<2; i++){
        int j = row + i;
        if (in_data.size() > j && j >= 0){
            string s = in_data[j].substr(beg, len);
            if (regex_search(s, m, e)){
                return true;
            }
        }
    }
    return false;
}

int adjacent_numb(int row, int beg, vector<string> &in_data){
    // check if stars have adjacent numbers
    // return gear number if 2 adjacent.
    // set search space in row
    int len = 1; 
    if (beg > 0){beg--; len ++;}
    if (beg + len < in_data[0].length()){len++;}

    regex e("[\\d]+");
    smatch m;
    int n = 0;
    int gear_ratio = 1;

    // check rows, if it exists
    for (int i = -1; i<2; i++){
        int j = row + i;
        if (in_data.size() > j && j >= 0){
            string s = in_data[j].substr(beg, len);

            int k = beg;
            while (regex_search(s, m, e)){
                n++;
                if (n > 2){return 0;}

                int l_bound = in_data[j].find_last_not_of("0123456789", m.position(0) + k);
                l_bound ++; // string::npos is -1. Always add one to get to the number.

                string s_num = in_data[j].substr(l_bound);
                smatch m_num;
                regex_search(s_num, m_num, e);
                gear_ratio *= stoi(m_num.str(0));          

                s = m.suffix().str();
                k += m.position(0) + m.length(0); 
            }
        }
    }
    if (n == 2){ return gear_ratio;}
    return 0;
}

int main () {

    string line;
    ifstream read_file;
    int sum_p1 = 0, sum_p2 = 0;
    vector<string> in_data;

    read_file.open ("input");

    if (read_file.is_open()){
        while ( getline(read_file, line)){
            in_data.push_back(line);
        }
        read_file.close();
    }

    // scan for numbers in rows
    int n = in_data.size();
    regex e ("[\\d]+");
    regex f ("(\\*)");

    for (unsigned i=0; i<n; i++){
        string row = in_data[i];
        smatch nums;
        smatch stars;
        int j = 0;
        while (regex_search(row, nums, e)) {

            if (adjacent_symb(i, nums.position(0) + j, nums.length(0), in_data)){
                sum_p1 += stoi(nums.str(0));
            }
            j += nums.position(0) + nums.length(0);
            row = nums.suffix().str();
        }

        row = in_data[i];
        int k = 0;
        while (regex_search(row, stars, f)) {
            sum_p2 += adjacent_numb(i, stars.position(0) + k, in_data);
            k += stars.position(0) + 1;
            row = stars.suffix().str();
        }
    }

    std::cout << "Day 3 part 1: " << sum_p1 << '\n';
    std::cout << "Day 3 part 2: " << sum_p2 << '\n';
    return 0;
}

