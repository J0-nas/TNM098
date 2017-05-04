
#pragma once

#include <vector>
#include <string>
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

  void initCarInfo(string id, int type) {
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

private:
  int duration{};
  string car_id{};
  int car_type{};
  vector<tuple<int, string>> locations{};
};
