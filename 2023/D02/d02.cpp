// Michael Chen
// Advent of Code 2023 Day 2 part 1 and 2
// 12/2/2023

#include <iostream>
#include <fstream>
#include <string>
#include <array>
using namespace std;
#define R_MAX 12
#define G_MAX 13
#define B_MAX 14

bool check_max(string hand){
    // checks the cubes in hand against the defined maximum values in game. 
    // return true if the hand was possible. 
    array<int, 3> max_array = {R_MAX, G_MAX, B_MAX};
    string colors[] = {"red", "green", "blue"};

    for (int i=0; i < 3; i++){

        size_t pos = hand.find(colors[i]);
        if (pos == string::npos){continue;}

        string color_str = hand.substr(0,pos);
        pos = color_str.find_last_of(' ');
        color_str = color_str.substr(0, pos);
        pos = color_str.find_last_of(' ') + 1; // in case of npos -1, +1 makes 0.
        color_str = color_str.substr(pos);

        int color_int = stoi(color_str);
        if (color_int > max_array[i]){
            return false;
        }
    }
    return true;
}

pair<string, string> parse_hand(string game){
    // returns the first "hand" in a line and the remaining hands substring.
    int sub_str_end = game.find_first_of(';');
    if (sub_str_end == string::npos){sub_str_end = game.length()-1;}
    int sub_str_beg = game.find_first_not_of(' ');

    return make_pair(game.substr(sub_str_beg, sub_str_end), game.substr(sub_str_end+1));
}

bool valid_game(string line){
    // takes a line, prunes the game number off, then validates the game.
    int sub_game_beg = line.find_first_of(':');
    string game = line.substr(sub_game_beg + 1);
    pair <string, string> hand;

    while (true) {
        hand = parse_hand(game);

        if (!check_max(hand.first)){ return false;};

        game = hand.second;
        if (game.length() < 2){
            return true;
        }
    }
}

void color_nums(string hand, int* color_nums){
    // writes into colornums an array of numbers representing r,g,b in the game.
    string colors[] = {"red", "green", "blue"};

    for (int i=0; i < 3; i++){

        size_t pos = hand.find(colors[i]);
        if (pos == string::npos){continue;}

        string color_str = hand.substr(0,pos);
        pos = color_str.find_last_of(' ');
        color_str = color_str.substr(0, pos);
        pos = color_str.find_last_of(' ') + 1; // in case of npos -1, +1 makes 0.
        color_str = color_str.substr(pos);

        color_nums[i] = stoi(color_str);
    }
}

int power_game(string line){
    // Takes a line and then does part 2 to find the 'power' of a minimum 
    // set of colors for a game to be valid.
    
    int min_array[3] = {0,0,0};
    int hand_nums[3] = {0,0,0};

    bool start = true;
    string colors[] = {"red", "green", "blue"};

    int sub_game_beg = line.find_first_of(':');
    string game = line.substr(sub_game_beg + 1);
    pair <string, string> hand;

    while (true) {
        hand = parse_hand(game);

        color_nums(hand.first, hand_nums);
        for (int i = 0; i < 3; i++){
            min_array[i] = max(min_array[i], hand_nums[i]);
        }

        game = hand.second;
        if (game.length() < 2){
            return min_array[0]*min_array[1]*min_array[2];
        }
    }
}

int main () {

    string line;
    ifstream input;
    int sum_p1 = 0, n = 0, sum_p2 = 0;

    input.open ("input");

    if (input.is_open()){
        while ( getline(input, line)){
            n++;
            if (valid_game(line)){
                sum_p1 += n;
            }
            sum_p2 += power_game(line);
        }
        input.close();
    }

    cout << "Day 2 part 1: " << sum_p1 << '\n';
    cout << "Day 2 part 2: " << sum_p2 << '\n';
    return 0;
}