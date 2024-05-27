#include <iostream>
#include <string>
#include <vector>
#include <sstream> // Включаем заголовочный файл для std::istringstream

using namespace std;

// Функция для разбиения строки по разделителю
vector<string> split(const string& s, char delimiter) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Функция для определения класса IP-адреса
char findClass(const string& ip_address) {
    vector<string> octets = split(ip_address, '.');
    int first_octet = stoi(octets[0]);

    if (first_octet >= 1 && first_octet <= 126) {
        return 'A';
    } else if (first_octet >= 128 && first_octet <= 191) {
        return 'B';
    } else if (first_octet >= 192 && first_octet <= 223) {
        return 'C';
    } else if (first_octet >= 224 && first_octet <= 239) {
        return 'D';
    } else {
        return 'E';
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <IP address>" << endl;
        return 1;
    }

    string ip_address = argv[1];

    char ip_class = findClass(ip_address);
    cout << "IP address " << ip_address << " belongs to class " << ip_class << endl;

    return 0;
}
