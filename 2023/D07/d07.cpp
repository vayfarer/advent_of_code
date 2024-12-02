// Michael Chen
// Advent of Code 2023 Day 7 part 1 and 2
// 12/24/2023

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <cmath>
#include <map>
#include <ctime>
#include <cctype>
#include <algorithm>    // std::sort
#include <tuple>
using namespace std;

int card_to_i (char c, bool joker){
    map<char, int> faces;
    faces ['A'] = 14;
    faces ['K'] = 13;
    faces ['Q'] = 12;
    faces ['J'] = (joker)?1:11;
    faces ['T'] = 10;

    if (isdigit(c)){
        return c - '0';
    } else {
        return faces[c];
    }
}

vector<int> hand_to_v(string hand, bool joker){
    vector <int> h_nums;
    for (char &c : hand){
        h_nums.push_back(card_to_i(c, joker));
    }
    return h_nums;
}

int vector_to_i(vector<int> hand){
    int nhand = 0;
    for (int i = 0; i < 5; i++){
        nhand += pow(16,(4-i)) * hand[i];
    }
    return nhand;
}

int rank_hand (vector<int> hand, bool joker){
    int num_kind1 = 0, num_kind2 = 0;
    map <int, int> h_map;

    for (int &n: hand){
        if (h_map.count(n)){h_map[n]++;} else {h_map[n] = 1;}
    }

    for(const auto& card : h_map){
        if (card.second > num_kind1){
            num_kind2 = num_kind1;
            num_kind1 = card.second;
        } else if (card.second > num_kind2) {
            num_kind2 = card.second;
        }
    }

    if (joker && h_map.count(1)){
        // has at least one joker
        if (h_map[1] <= num_kind2){
            // jokers are at most second most common. add to most common. 
            num_kind1 += h_map[1];
        } else {num_kind1 += num_kind2;} // else jokers are most common.
    }

    switch (num_kind1){
        case 5:
            return 6;
        case 4:
            return 5;
        case 3:
            if (num_kind2 == 2){return 4;} else {return 3;}
        case 2:
            if (num_kind2 == 2){return 2;} else {return 1;}
        case 1: 
            return 0;
        default:
            cout << "ERROR!!";
            return 0;            // how did you get here??
    }
}

bool h_less_than (tuple<int, int, int> hand1, tuple<int, int, int> hand2) {
    // true if hand1 is greater than hand2.
    if (get<1>(hand1) > get<1>(hand2)){
        return false;
    }
    
    if (get<1>(hand1) == get<1>(hand2)) {
        return (get<2>(hand1) > get<2>(hand2))? false : true;
    }

    return true;
}

int main () {

    clock_t timer = clock();

    string line;
    ifstream read_file;
    int p1 = 0, p2 = 0;
    vector<tuple<int, int, int>> hands, hands_p2;

    read_file.open ("input");
    if (read_file.is_open()){
        regex e ("(\\w+) (\\d+)");
        smatch hand;
        while(getline(read_file, line)){
            regex_match(line, hand, e);
            vector<int> vector_hand = hand_to_v(hand.str(1),false);
            vector<int> vector_hand_p2 = hand_to_v(hand.str(1),true);
            hands.push_back(make_tuple(stoi(hand.str(2)), 
            rank_hand(vector_hand, false), vector_to_i(vector_hand)));
            hands_p2.push_back(make_tuple(stoi(hand.str(2)), 
            rank_hand(vector_hand_p2, true), vector_to_i(vector_hand_p2)));
        }
        read_file.close();
    }    

    sort(hands.begin(), hands.end(), h_less_than);
    for (int i = 0; i < hands.size(); i++){
        p1 += (i+1) * get<0>(hands[i]);
    }

    sort(hands_p2.begin(), hands_p2.end(), h_less_than);
    for (int i = 0; i < hands_p2.size(); i++){
        p2 += (i+1) * get<0>(hands_p2[i]);
    }

    timer = clock() - timer;
    cout << "runtime: " << (float)timer/CLOCKS_PER_SEC * 1000 << "ms \n";
    
    cout << "Day 7 part 1: " << p1 << '\n';
    cout << "Day 7 part 2: " << p2 << '\n';

    return 0;
}