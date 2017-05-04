#pragma once

#include <vector>
#include <iterator>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <ctime>

//#include "path.cpp"

using namespace std;

class WordDelimitedByComma : public string
{};

istream& operator>>(istream& is, WordDelimitedByComma& output)
{
   getline(is, output, ',');
   return is;
}

class DataPoint {
public:
  DataPoint(DataPoint& other) {
    time_stamp = other.time_stamp;
    car_id = other.car_id;
    car_type = other.car_type;
    checkpoint_id = other.checkpoint_id;
    cout << "copy constructor" << endl;
  }

  DataPoint(DataPoint&& other) {
    time_stamp = other.time_stamp;
    car_id = other.car_id;
    car_type = other.car_type;
    checkpoint_id = other.checkpoint_id;
    
    //cout << "in move constructor" << endl;
    other.time_stamp = -1;
    other.car_id = "";
    other.car_type = -1;
    other.checkpoint_id = "";
  }
  
  DataPoint(string csv_line) {
    istringstream iss(csv_line);
    vector<string> words {istream_iterator<WordDelimitedByComma>{iss}, istream_iterator<WordDelimitedByComma>{}};
    int c_t = stoi(words[2]);
    //copy(words.begin(), words.end(), ostream_iterator<string>{cout, ", "});
    //cout << endl;

    istringstream time_reader {words[0]};
    tm t{0};
    time_reader >> get_time(&t, "%Y-%m-%d %H:%M:%S");
    //strptime(words[0], "%Y-%m-%d %H:%M-%S", &t);

    //istringstream ss("2014 11 05 T 12 34 56");
    //ss >> get_time(&t, "%Y %m %d T %H %M %S");
    
    time_stamp = mktime(&t);
    
    car_id = words[1];
    car_type = c_t;
    checkpoint_id = words[3];
    //cout << "string constructor" << endl;
  }

  DataPoint(int t_s, string c_i, int c_t, string check_i):
    time_stamp {t_s}, car_id{c_i}, car_type {c_t}, checkpoint_id {check_i}
  {
    //cout << time_stamp << endl;
    cout << "regular constructor" << endl;
  }

  string getSummary() {
    return "t_s: " + to_string(time_stamp) + " c_i: " + car_id + " c_t: " + to_string(car_type) + " c_i: " + checkpoint_id;
  }

  string getIdentifier() {
    return string{car_id};
  }

  int getTime() {
    return time_stamp;
  }

  string getLocation() {
    return checkpoint_id;
  }
    
private:
  int time_stamp{};
  string car_id{};
  int car_type{};
  string checkpoint_id{};

  friend class Path;
};
