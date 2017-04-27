#include <vector>
#include <iterator>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>

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
  DataPoint(string csv_line) {
    istringstream iss(csv_line);
    vector<string> words {istream_iterator<WordDelimitedByComma>{iss}, istream_iterator<WordDelimitedByComma>{}};
    int c_t = stoi(words[2]);
    //copy(words.begin(), words.end(), ostream_iterator<string>{cout, ", "});
    //cout << endl;
    
    time_stamp = words[0];
    car_id = words[1];
    car_type = c_t;
    checkpoint_id = words[3];
      //DataPoint(move(words[0]), words[1], c_t, words[3]);
  }

  DataPoint(string t_s, string c_i, int c_t, string check_i):
    time_stamp {move(t_s)}, car_id{c_i}, car_type {c_t}, checkpoint_id {check_i}
  {
    cout << time_stamp << endl;
  }

  string getSummary() {
    return "t_s: " + time_stamp + " c_i: " + car_id + " c_t: " + to_string(car_type) + " c_i: " + checkpoint_id;
  }
  
private:
  string time_stamp{};
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
  while(getline(ifs, line)) {
    //cout << line << endl;
    
    //points.push_back(DataPoint{line});
    DataPoint tmp {line};
    points.push_back(DataPoint{line});
  }
  cout << points.at(0).getSummary() << endl;
  cout << points.back().getSummary() << endl;
}
