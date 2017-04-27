#include <vector>
#include <iterator>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <ctime>


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
  }

  DataPoint(int t_s, string c_i, int c_t, string check_i):
    time_stamp {t_s}, car_id{c_i}, car_type {c_t}, checkpoint_id {check_i}
  {
    cout << time_stamp << endl;
  }

  string getSummary() {
    return "t_s: " + to_string(time_stamp) + " c_i: " + car_id + " c_t: " + to_string(car_type) + " c_i: " + checkpoint_id;
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
  while(getline(ifs, line)) {
    DataPoint tmp {line};
    points.push_back(DataPoint{line});
  }

  
  cout << points.at(0).getSummary() << endl;
  cout << points.back().getSummary() << endl;
}
