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
  for (auto & n: m) {
    //for (auto & i: n.second) {
      //cout << i.getSummary() << endl;
    //}
    car_id{n};
    int start{n.second.front().getTime()};
    int end{n.second.back().getTime()};
    int diff = end-start;
    if (diff > 60*60*24) {
      cout << n.first << endl;
      cout << "\t\tMore than 24h: " << (diff/60) << " min." << endl;
      for (auto & i: n.second) {
	cout << i.getLocation() << endl;
      }
    }
  }
  cout << car_id << endl;
  Path p{m[car_id]};
  
  //cout << "points" << endl;
  //for (auto & d: points) {
  //  cout << d.getLocation() << endl;
  //}
  //copy(m.begin(), m.end(), ostream_iterator<vector<DataPoint>>{cout});
}
