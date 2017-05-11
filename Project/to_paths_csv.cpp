#include <vector>
#include <map>
#include <iterator>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <utility>

#include <typeinfo>

#include "datapoint.cpp"
#include "path.cpp"

using namespace std;

int main(int argc, char** argv) {
  ifstream ifs {argv[1]};
  string line {};
  getline(ifs, line);
  cout << line << endl;
  vector<DataPoint> points {};
  int i = 0;
  while(getline(ifs, line) && i < 30) {
    points.push_back(move(DataPoint{line}));
    i --;
  }
  cout << "\tvector built" << endl;
  
  //cout << points.at(0).getSummary() << endl;
  //cout << points.back().getSummary() << endl;
  
  /*
  DataPoint a{2016, "i_a", 5, "check_a"};
  DataPoint b{2016, "i_b", 6, "check_b"};
  cout << a.getSummary() << endl;
  cout << b.getSummary() << endl;
  auto c = DataPoint{a};
  cout << a.getSummary() << endl;
  cout << c.getSummary() << endl;
  auto d = move(a);
  cout << a.getSummary() << endl;
  cout << d.getSummary() << endl;
  cout << "-----------" << endl;
  map<string, vector<DataPoint>> m {};
  //m["i"] = vector<DataPoint>{};
  //m["i"].push_back(DataPoint{move(d)});
  //cout << d.getSummary() << endl;
  */
  map<string, vector<DataPoint>> m {};
  for (auto & i: points) {
    if (m.find(i.getIdentifier()) == m.end()) {
      m[i.getIdentifier()] = vector<DataPoint>{};
    }
    m[i.getIdentifier()].push_back(move(i));
  }
  cout << "\tmap built" << endl;

  string car_id{};
  vector<Path> paths{};
  vector<Path> multi_day_paths{};
  for (auto & n: m) {
    //for (auto & i: n.second) {
      //cout << i.getSummary() << endl;
    //}
    car_id = string{n.first};
    int start{n.second.front().getTime()};
    int end{n.second.back().getTime()};
    int diff = end-start;
    //add >1 day paths
    if (diff > 60*60*24) {
      multi_day_paths.push_back(Path{});
      multi_day_paths.back().initCarInfo(n.second.front().getIdentifier(), n.second.front().getCarType());
      for (auto & p: n.second) {
	multi_day_paths.back().addLocation(make_tuple(p.getTime(), p.getLocation()));
      }
      // Add <1 day path
    } else {
      paths.push_back(Path{});
      paths.back().initCarInfo(n.second.front().getIdentifier(), n.second.front().getCarType());
      for (auto & p: n.second) {
	paths.back().addLocation(make_tuple(p.getTime(), p.getLocation()));
      }
    }
  }
  cout << car_id << endl;
  //cout << typeid(m[car_id]).name() << endl;
  //Path p{m[car_id].front()};

  map<string, int> pathCount{};
  for (auto& p : paths) {
    if (pathCount.find(p.getPathLocString()) == pathCount.end()) {
      pathCount[p.getPathLocString()] = 1;
    } else {
      pathCount[p.getPathLocString()] = pathCount[p.getPathLocString()] + 1;
    }
  }

  for (auto& c: pathCount) {
    //cout << "\t" << c.second << endl;
  }
  cout << paths.size() << endl;
  cout << multi_day_paths.size() << endl;

  ofstream s1{};
  s1.open("single_day_paths.csv");
  for (auto& p: paths) {
    s1 << p.buildCSVString() << endl;
  }
  s1.close();

  ofstream s2{};
  s2.open("multi_day_paths.csv");
  for (auto& p: multi_day_paths) {
    s2 << p.buildCSVString() << endl;
  }
  
  //cout << "points" << endl;
  //for (auto & d: points) {
  //  cout << d.getLocation() << endl;
  //}
  //copy(m.begin(), m.end(), ostream_iterator<vector<DataPoint>>{cout});
}
