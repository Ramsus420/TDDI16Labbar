#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <algorithm>

using std::vector;
using std::string;
using std::cout;
using std::endl;

// Typ som används för ordlistan. Den definieras med en typedef här så att du enkelt kan ändra
// representationen av en ordlista utefter vad din implementation behöver. Funktionen
// "read_questions" skickar ordlistan till "find_shortest" och "find_longest" med hjälp av denna
// typen.
typedef std::unordered_set<string> Dictionary;

/**
 * Hitta den kortaste ordkedjan från 'first' till 'second' givet de ord som finns i
 * 'dict'. Returvärdet är den ordkedja som hittats, första elementet ska vara 'from' och sista
 * 'to'. Om ingen ordkedja hittas kan en tom vector returneras.
 */

vector<string> find_neighbours(const Dictionary &dict, const string &word) {
    vector<string> neighbours;
    for (size_t i {0}; i < word.size(); i++){
        string temp = word;
        for (char c = 'a'; c <= 'z'; c++){
            temp[i] = c;
            if (temp != word && dict.find(temp) != dict.end()){
                neighbours.push_back(temp);
            }
        }
    }
    return neighbours;
}

vector<string> find_shortest(const Dictionary &dict, const string &from, const string &to) {
    // Check if 'from' or 'to' are not in the dictionary
    if (dict.find(from) == dict.end() || dict.find(to) == dict.end()) {
        return {};
    }

    vector<string> result;
    std::unordered_set<string> visited;
    std::unordered_map<string, string> parent;
    std::queue<string> q;
    q.push(from);
    visited.insert(from);
    while (!q.empty()){
        string current = q.front();
        q.pop();
        if (current == to){
            string temp = current;
            while (temp != from){
                result.push_back(temp);
                temp = parent[temp];
            }
            result.push_back(from);
            std::reverse(result.begin(), result.end());
            return result;
        }
        vector<string> neighbours = find_neighbours(dict, current);
        for (size_t i = 0; i < neighbours.size(); i++){
            if (visited.find(neighbours[i]) == visited.end()){
                visited.insert(neighbours[i]);
                parent[neighbours[i]] = current;
                q.push(neighbours[i]);
            }
        }
    }
    return {};
}

/**
 * Hitta den längsta kortaste ordkedjan som slutar i 'word' i ordlistan 'dict'. Returvärdet är den
 * ordkedja som hittats. Det sista elementet ska vara 'word'.
 */

vector<string> find_longest(const Dictionary &dict, const string &word) {
    if (dict.find(word) == dict.end()){
        return {};
    }

    vector<string> result;
    std::unordered_map<string, int> distance;
    std::unordered_map<string, string> parent;
    std::queue<string> q;

    
    q.push(word);
    distance[word] = 0;
    while (!q.empty()){
        string current = q.front();
        q.pop();
        vector<string> neighbours = find_neighbours(dict, current);
        for (size_t i = 0; i < neighbours.size(); i++){
            if (distance.find(neighbours[i]) == distance.end()){
                distance[neighbours[i]] = distance[current] + 1;
                parent[neighbours[i]] = current;
                q.push(neighbours[i]);
            }
        }
    }

    //hitta ordet med längst avstånd
    int max_distance = 0;
    string max_word = word;
    for (auto it = distance.begin(); it != distance.end(); it++){
        if (it->second > max_distance){
            max_distance = it->second;
            max_word = it->first;
        }
    }

    //skapa ordkedjan med max_word
    string temp = max_word;
    while (temp != word){
        result.push_back(temp);
        temp = parent[temp];
    }
    result.push_back(word);

    return result;
}


/**
 * Läs in ordlistan och returnera den som en vector av orden. Funktionen läser även bort raden med
 * #-tecknet så att resterande kod inte behöver hantera det.
 */
Dictionary read_dictionary() {
    string line;
    vector<string> result;
    while (std::getline(std::cin, line)) {
        if (line == "#")
            break;

        result.push_back(line);
    }

    return Dictionary(result.begin(), result.end());
}

/**
 * Skriv ut en ordkedja på en rad.
 */
void print_chain(const vector<string> &chain) {
    if (chain.empty())
        return;

    vector<string>::const_iterator i = chain.begin();
    cout << *i;

    for (++i; i != chain.end(); ++i)
        cout << " -> " << *i;

    cout << endl;
}

/**
 * Skriv ut ": X ord" och sedan en ordkedja om det behövs. Om ordkedjan är tom, skriv "ingen lösning".
 */
void print_answer(const vector<string> &chain) {
    if (chain.empty()) {
        cout << "ingen lösning" << endl;
    } else {
        cout << chain.size() << " ord" << endl;
        print_chain(chain);
    }
}

/**
 * Läs in alla frågor. Anropar funktionerna "find_shortest" eller "find_longest" ovan när en fråga hittas.
 */
void read_questions(const Dictionary &dict) {
    string line;
    while (std::getline(std::cin, line)) {
        size_t space = line.find(' ');
        if (space != string::npos) {
            string first = line.substr(0, space);
            string second = line.substr(space + 1);
            vector<string> chain = find_shortest(dict, first, second);

            cout << first << " " << second << ": ";
            print_answer(chain);
        } else {
            vector<string> chain = find_longest(dict, line);

            cout << line << ": ";
            print_answer(chain);
        }
    }
}

int main() {
    Dictionary dict = read_dictionary();
    
    
    read_questions(dict);

    return 0;
}
