#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <iomanip>
#include <cctype>

using namespace std;

string encryptionKey = "QWERTYUIOPASDFGHJKLZXCVBNM";

string read_file(string filename)
{
    ifstream file(filename);

    if (!file)
    {
        cout << "Unable to open " << filename << endl;
        return "";
    }

    string text;
    string line;

    while (getline(file, line))
    {
        text += line;
        text += '\n';
    }

    file.close();

    return text;
}

string encrypt_text(string plaintext)
{
    string ciphertext = "";

    for (char ch : plaintext)
    {
        if (isalpha(ch))
        {
            bool upper = isupper(ch);

            char plain = toupper(ch);

            int index = plain - 'A';

            char cipher = encryptionKey[index];

            if (!upper)
                cipher = tolower(cipher);

            ciphertext += cipher;
        }
        else
        {
            ciphertext += ch;
        }
    }

    return ciphertext;
}

void frequency_analysis(string ciphertext)
{
    int frequency[26] = {0};
    int totalLetters = 0;

    for (char ch : ciphertext)
    {
        if (isalpha(ch))
        {
            ch = toupper(ch);

            frequency[ch - 'A']++;

            totalLetters++;
        }
    }

    vector<pair<char, int>> result;

    for (int i = 0; i < 26; i++)
    {
        result.push_back({char('A' + i), frequency[i]});
    }

    sort(result.begin(), result.end(),
    [](pair<char, int> a, pair<char, int> b)
    {
        return a.second > b.second;
    });

    cout << "\nLETTER FREQUENCY ANALYSIS\n";

    cout << left
         << setw(10) << "Letter"
         << setw(10) << "Count"
         << "Percentage\n";

    cout << "--------------------------------\n";

    for (auto p : result)
    {
        double percentage = 0;

        if (totalLetters != 0)
            percentage = (p.second * 100.0) / totalLetters;

        cout << left
             << setw(10) << p.first
             << setw(10) << p.second
             << fixed << setprecision(2)
             << percentage << "%\n";
    }

    if (!result.empty())
    {
        cout << "\nMost frequent ciphertext letter: "
             << result[0].first
             << endl;
    }
}

vector<string> extract_words(string text)
{
    vector<string> words;

    string word = "";

    for (char ch : text)
    {
        if (isalpha(ch))
        {
            word += toupper(ch);
        }
        else
        {
            if (!word.empty())
            {
                words.push_back(word);
                word = "";
            }
        }
    }

    if (!word.empty())
        words.push_back(word);

    return words;
}

void word_frequency_analysis(string ciphertext)
{
    vector<string> words = extract_words(ciphertext);

    map<string, int> wordCount;

    for (string word : words)
    {
        wordCount[word]++;
    }

    cout << "\nONE LETTER WORDS\n";

    for (auto p : wordCount)
    {
        if (p.first.length() == 1)
        {
            cout << p.first
                 << " -> "
                 << p.second
                 << endl;
        }
    }

    cout << "\nTWO LETTER WORDS\n";

    for (auto p : wordCount)
    {
        if (p.first.length() == 2)
        {
            cout << p.first
                 << " -> "
                 << p.second
                 << endl;
        }
    }

    cout << "\nTHREE LETTER WORDS\n";

    for (auto p : wordCount)
    {
        if (p.first.length() == 3)
        {
            cout << p.first
                 << " -> "
                 << p.second
                 << endl;
        }
    }

    cout << "\nREPEATED WORDS\n";

    vector<pair<string, int>> repeated;

    for (auto p : wordCount)
    {
        if (p.second > 1)
        {
            repeated.push_back(p);
        }
    }

    sort(repeated.begin(), repeated.end(),
    [](pair<string, int> a, pair<string, int> b)
    {
        return a.second > b.second;
    });

    for (auto p : repeated)
    {
        cout << setw(20)
             << left
             << p.first
             << p.second
             << endl;
    }
}

string generate_pattern(string word)
{
    map<char, int> positions;

    int nextNumber = 0;

    string pattern = "";

    for (char ch : word)
    {
        if (positions.find(ch) == positions.end())
        {
            positions[ch] = nextNumber;
            nextNumber++;
        }

        pattern += to_string(positions[ch]);
        pattern += " ";
    }

    return pattern;
}

void pattern_analysis(string ciphertext)
{
    vector<string> words = extract_words(ciphertext);

    map<string, int> wordCount;

    for (string word : words)
    {
        wordCount[word]++;
    }

    cout << "\nWORD PATTERN ANALYSIS\n";

    cout << left
         << setw(20) << "Word"
         << setw(10) << "Count"
         << "Pattern\n";

    cout << "--------------------------------------------------\n";

    for (auto p : wordCount)
    {
        cout << left
             << setw(20) << p.first
             << setw(10) << p.second
             << generate_pattern(p.first)
             << endl;
    }
}

string apply_substitution(
    string ciphertext,
    map<char, char> substitution)
{
    string result = "";

    for (char ch : ciphertext)
    {
        if (isalpha(ch))
        {
            bool upper = isupper(ch);

            char cipher = toupper(ch);

            if (substitution.find(cipher)
                != substitution.end())
            {
                char plain = substitution[cipher];

                if (!upper)
                    plain = tolower(plain);

                result += plain;
            }
            else
            {
                result += '_';
            }
        }
        else
        {
            result += ch;
        }
    }

    return result;
}

void display_partial_plaintext(
    string ciphertext,
    map<char, char> substitution)
{
    string partial =
        apply_substitution(ciphertext, substitution);

    cout << "\nPARTIAL PLAINTEXT\n";
    cout << partial << endl;
}

bool verify_solution(
    string recoveredPlaintext,
    string originalCiphertext,
    string recoveredEncryptionKey)
{
    string encrypted = "";

    for (char ch : recoveredPlaintext)
    {
        if (isalpha(ch))
        {
            bool upper = isupper(ch);

            char plain = toupper(ch);

            int index = plain - 'A';

            char cipher =
                recoveredEncryptionKey[index];

            if (!upper)
                cipher = tolower(cipher);

            encrypted += cipher;
        }
        else
        {
            encrypted += ch;
        }
    }

    return encrypted == originalCiphertext;
}

string create_encryption_key(
    map<char, char> substitution)
{
    string key(26, '_');

    for (auto p : substitution)
    {
        char cipher = p.first;
        char plain = p.second;

        key[plain - 'A'] = cipher;
    }

    return key;
}

void display_substitutions(
    map<char, char> substitution)
{
    cout << "\nCURRENT SUBSTITUTIONS\n";

    cout << "Cipher : ";

    for (char c = 'A'; c <= 'Z'; c++)
        cout << c << " ";

    cout << "\nPlain  : ";

    for (char c = 'A'; c <= 'Z'; c++)
    {
        if (substitution.find(c)
            != substitution.end())
        {
            cout << substitution[c] << " ";
        }
        else
        {
            cout << "_ ";
        }
    }

    cout << endl;
}

void manual_cryptanalysis(string ciphertext)
{
    map<char, char> substitution;

    while (true)
    {
        cout << "\nCRYPTANALYSIS MENU\n";

        cout << "1. Add substitution\n";
        cout << "2. Remove substitution\n";
        cout << "3. Display partial plaintext\n";
        cout << "4. Display substitution table\n";
        cout << "5. Finish cryptanalysis\n";

        cout << "Enter choice: ";

        int choice;

        cin >> choice;

        if (choice == 1)
        {
            char cipherLetter;
            char plainLetter;

            cout << "Ciphertext letter: ";
            cin >> cipherLetter;

            cout << "Possible plaintext letter: ";
            cin >> plainLetter;

            cipherLetter =
                toupper(cipherLetter);

            plainLetter =
                toupper(plainLetter);

            bool conflict = false;

            for (auto p : substitution)
            {
                if (p.second == plainLetter &&
                    p.first != cipherLetter)
                {
                    conflict = true;
                }
            }

            if (conflict)
            {
                cout << "Plaintext letter "
                     << plainLetter
                     << " is already assigned.\n";
            }
            else
            {
                substitution[cipherLetter]
                    = plainLetter;

                cout << "Testing "
                     << cipherLetter
                     << " -> "
                     << plainLetter
                     << endl;

                display_partial_plaintext(
                    ciphertext,
                    substitution);
            }
        }

        else if (choice == 2)
        {
            char cipherLetter;

            cout << "Enter ciphertext letter: ";

            cin >> cipherLetter;

            cipherLetter =
                toupper(cipherLetter);

            substitution.erase(
                cipherLetter);

            cout << "Substitution removed.\n";
        }

        else if (choice == 3)
        {
            display_partial_plaintext(
                ciphertext,
                substitution);
        }

        else if (choice == 4)
        {
            display_substitutions(
                substitution);
        }

        else if (choice == 5)
        {
            string key =
                create_encryption_key(
                    substitution);

            cout << "\nRecovered encryption key:\n";

            cout << "Plain  : ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";

            cout << "Cipher : "
                 << key
                 << endl;

            break;
        }

        else
        {
            cout << "Invalid choice\n";
        }
    }
}

int main()
{
    string plaintext =
        read_file("plaintext.txt");

    if (plaintext.empty())
    {
        cout << "Plaintext file is empty or missing.\n";
        return 0;
    }

    cout << "\nORIGINAL PLAINTEXT\n";
    cout << plaintext << endl;

    cout << "\nENCRYPTION KEY\n";

    cout << "Plain  : ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";

    cout << "Cipher : "
         << encryptionKey
         << endl;

    string ciphertext =
        encrypt_text(plaintext);

    cout << "\nCIPHERTEXT\n";
    cout << ciphertext << endl;

    ofstream output("ciphertext.txt");

    output << ciphertext;

    output.close();

    frequency_analysis(ciphertext);

    word_frequency_analysis(ciphertext);

    pattern_analysis(ciphertext);

    manual_cryptanalysis(ciphertext);

    return 0;
}
