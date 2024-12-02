// Michael Chen
// Advent of Code 2023 Day 11 part 1 and 2
// 1/4/2024

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

class Galaxy{
    public:
        int x, y;

        Galaxy(int row, int col){
            x = col;
            y = row;
        }

        int manhattan(Galaxy other, unordered_set<int> rows_empty, unordered_set<int> cols_empty, int expand_dist = 2){
            int sml_x, sml_y, big_x, big_y;
            if (other.x > x){sml_x = x; big_x = other.x;}
            else {sml_x = other.x; big_x = x;}
            if (other.y > y){sml_y = y; big_y = other.y;}
            else {sml_y = other.y; big_y = y;}

            int expand_rows = big_y - sml_y, expand_columns = big_x - sml_x;

            for (int emp_x: cols_empty){
                if (sml_x < emp_x && big_x > emp_x){expand_columns += expand_dist - 1;}
            }
            for (int emp_y: rows_empty){
                if (sml_y < emp_y && big_y > emp_y){expand_rows += expand_dist - 1;}
            }

            return expand_columns + expand_rows;
        }
};

int main () {
    clock_t timer = clock();
    string line;
    ifstream read_file;
    int p1 = 0; long p2 = 0;
    vector <string> image;

    read_file.open ("input");
    if (read_file.is_open()){
        while(getline(read_file, line)){
            image.push_back(line);
        }
        read_file.close();
    }    

    // sets of possible empty space
    unordered_set <int> rows_empty, cols_empty;

    // empty rows
    for (int i = 0; i < image.size(); i++){
        regex e ("(#)");
        smatch sm;
        if (!regex_search(image[i], sm, e)){
            rows_empty.emplace(i);
        }
    }

    // empty columns
    for (int i = 0; i < image[0].size(); i++){
        bool no_galaxy = true;
        int j = 0;
        while (no_galaxy && j < image.size()){
            if (image[j][i] == '#'){
                no_galaxy = false;
            }
            j++;
        }
        if (no_galaxy){
            cols_empty.emplace(i);
        }
    }

    // locate all galaxies
    vector <Galaxy> galaxies;
    for (int i = 0; i < image.size(); i++){
        string row = image[i];
        regex e ("(#)");
        smatch sm;
        int offset = 0;
        while(regex_search(row, sm, e)){
            Galaxy galobj(i, sm.position() + offset);
            galaxies.push_back(galobj);
            
            offset += sm.position() + 1;
            row = sm.suffix().str();
        }
    }

    // calculate distance between all galaxies
    for (int i = 0; i < galaxies.size(); i++){
        for (int j = i; j < galaxies.size(); j++){
            p1 += galaxies[i].manhattan(galaxies[j], rows_empty, cols_empty);
            p2 += galaxies[i].manhattan(galaxies[j], rows_empty, cols_empty, 1000000);
        }
    }

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 11 part 1: " << p1 << '\n';
    cout << "Day 11 part 2: " << p2 << '\n';

    return 0;
}