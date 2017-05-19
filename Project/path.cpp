
#pragma once

#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <tuple>

#include "datapoint.cpp"

using namespace std;

class Path {
public:
  Path() {}
  Path(DataPoint & point) :
    duration{0},
    car_id{point.car_id},
    car_type{point.car_type},
    locations{vector<tuple<int,string>>{make_tuple(point.time_stamp, point.checkpoint_id)}}
    {}

  //Assumes the new location to be visited after the last one...
  void addLocation(tuple<int, string> loc_pair) {
    locations.push_back(loc_pair);
    duration  = get<0>(locations.back()) - get<0>(locations.front());
  }

  void initCarInfo(string id, string type) {
    car_id = id;
    car_type = type;
  }

  string getPathLocString() {
    string res{""};
    for (auto & loc: locations) {
      res.append(get<1>(loc));
      res.append(" ");
    }
    return res;
  }

  int getPathDescription() {
    return 0;
  }

  int getPathLength() {
    return locations.size();
  }

  string buildCSVString() {
    stringstream ss{};
    ss << car_id << "," << car_type << "," << to_string(duration);
    for (auto& l : locations) {
      ss << "," << to_string(get<0>(l)) << " " << get<1>(l);
    }
    //ss << endl;
    return ss.str();
  }

private:
  int duration{};
  string car_id{};
  string car_type{};
  vector<tuple<int, string>> locations{};
};
