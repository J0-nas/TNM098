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
  void addLocation(string loc) {
    locations.push_back(loc);
    duration  = get<0>(locations.back()) - get<0>(locations.front());
  }

private:
  int duration{};
  string car_id{};
  int car_type{};
  vector<tuple<int, string>> locations{};
};
