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
  
private:
  int time_stamp{};
  string car_id{};
  int car_type{};
  string checkpoint_id{};
};

int main(int argc, char** argv) {
  ifstream ifs {argv[1]};
  string line {};
  getline(ifs, line);
  cout << line << endl;
  vector<DataPoint> points {};
  int i = 0;
  while(getline(ifs, line) && i < 30) {
    points.push_back(move(DataPoint{line}));
    i ++;
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

  for (auto & n: m) {
    for (auto & i: n.second) {
      //cout << i.getSummary() << endl;
    }
  }

  cout << "points" << endl;
  for (auto & d: points) {
    cout << d.getSummary() << endl;
  }
  //copy(m.begin(), m.end(), ostream_iterator<vector<DataPoint>>{cout});
}
