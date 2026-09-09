#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>
#include <cmath>
using namespace std;


// 1. Remove spaces/special characters and convert to uppercase
string clean_ciphertext(string text)
{
    string cleaned = "";

    for(char ch : text)
    {
        if(isalpha(ch))
            cleaned += toupper(ch);
    }

    return cleaned;
}


// 2. Find repeated patterns of length 3
map<string, vector<int>> find_repeated_patterns(string text)
{
    map<string, vector<int>> patterns;

    int patternLength = 3;

    for(int i = 0; i <= text.length() - patternLength; i++)
    {
        string pattern = text.substr(i, patternLength);

        patterns[pattern].push_back(i);
    }

    // Remove patterns which occur only once
    for(auto it = patterns.begin(); it != patterns.end(); )
    {
        if(it->second.size() < 2)
            it = patterns.erase(it);
        else
            ++it;
    }

    return patterns;
}


// 3. Calculate distances between repeated patterns
vector<int> calculate_distances(map<string, vector<int>> patterns)
{
    vector<int> distances;

    cout << "\nRepeated Patterns and Distances\n";
    cout << "--\n";

    for(auto p : patterns)
    {
        vector<int> positions = p.second;

        cout << p.first << " : ";

        for(int pos : positions)
            cout << pos << " ";

        cout << "   Distances: ";

        for(int i = 0; i < positions.size() - 1; i++)
        {
            int distance = positions[i + 1] - positions[i];

            distances.push_back(distance);

            cout << distance << " ";
        }

        cout << endl;
    }

    return distances;
}


// 4. Find factors of distances
map<int, int> find_factors(vector<int> distances)
{
    map<int, int> factorCount;

    // We check reasonable Vigenere key lengths 2-20
    for(int distance : distances)
    {
        for(int factor = 2; factor <= 20; factor++)
        {
            if(distance % factor == 0)
                factorCount[factor]++;
        }
    }

    return factorCount;
}


// Calculate Index of Coincidence
double calculate_ic(string group)
{
    int frequency[26] = {0};

    for(char ch : group)
        frequency[ch - 'A']++;

    int n = group.length();

    if(n <= 1)
        return 0;

    double numerator = 0;

    for(int i = 0; i < 26; i++)
    {
        numerator += frequency[i] * (frequency[i] - 1);
    }

    return numerator / (n * (n - 1.0));
}


// Split ciphertext according to key length
vector<string> split_into_groups(string text, int keyLength)
{
    vector<string> groups(keyLength);

    for(int i = 0; i < text.length(); i++)
    {
        groups[i % keyLength] += text[i];
    }

    return groups;
}


// 5. Kasiski analysis + IC
int kasiski_analysis(string text)
{
    map<string, vector<int>> patterns =
        find_repeated_patterns(text);

    vector<int> distances =
        calculate_distances(patterns);

    map<int, int> factorCount =
        find_factors(distances);

    cout << "\nFactor Frequencies\n";
    cout << "--\n";

    for(auto p : factorCount)
    {
        cout << "Factor " << p.first
             << " : " << p.second << endl;
    }

    int maximumFactorCount = 0;

    for(auto p : factorCount)
        maximumFactorCount =
            max(maximumFactorCount, p.second);

    /*
        Kasiski can give factors such as 2, 7, 14.

        We therefore use IC to decide which candidate
        is most likely to be the real key length.
    */

    double bestIC = 0;
    int bestLength = 1;

    cout << "\nCandidate Key Length IC Values\n";
    cout << "--\n";

    for(auto p : factorCount)
    {
        int keyLength = p.first;

        // Ignore very weak Kasiski candidates
        if(p.second < maximumFactorCount / 2)
            continue;

        vector<string> groups =
            split_into_groups(text, keyLength);

        double totalIC = 0;

        for(string group : groups)
            totalIC += calculate_ic(group);

        double averageIC =
            totalIC / keyLength;

        cout << "Length " << keyLength
             << " : IC = "
             << averageIC << endl;

        if(averageIC > bestIC)
        {
            bestIC = averageIC;
            bestLength = keyLength;
        }
    }

    return bestLength;
}


// 6. Frequency table for every group
vector<vector<int>> frequency_analysis(vector<string> groups)
{
    vector<vector<int>> allFrequencies;

    for(int g = 0; g < groups.size(); g++)
    {
        vector<int> frequency(26, 0);

        for(char ch : groups[g])
        {
            frequency[ch - 'A']++;
        }

        allFrequencies.push_back(frequency);

        cout << "\nGroup " << g + 1
             << " : " << groups[g] << endl;

        cout << "Letter\tFrequency\n";

        for(int i = 0; i < 26; i++)
        {
            cout << char('A' + i)
                 << "\t"
                 << frequency[i]
                 << endl;
        }

        cout << "IC = "
             << calculate_ic(groups[g])
             << endl;
    }

    return allFrequencies;
}


// Find Caesar shift using Chi-square frequency analysis
int find_shift(string group)
{
    /*
        Standard approximate English letter frequencies
    */

    double englishFrequency[26] =
    {
        8.2, 1.5, 2.8, 4.3, 12.7, 2.2,
        2.0, 6.1, 7.0, 0.15, 0.77, 4.0,
        2.4, 6.7, 7.5, 1.9, 0.095, 6.0,
        6.3, 9.1, 2.8, 0.98, 2.4, 0.15,
        2.0, 0.074
    };

    int observed[26] = {0};

    for(char ch : group)
        observed[ch - 'A']++;

    double bestScore = 1e100;
    int bestShift = 0;

    for(int shift = 0; shift < 26; shift++)
    {
        double chiSquare = 0;

        for(int cipherLetter = 0;
            cipherLetter < 26;
            cipherLetter++)
        {
            /*
                If key shift = shift:

                plaintext =
                ciphertext - shift
            */

            int plainLetter =
                (cipherLetter - shift + 26) % 26;

            double expected =
                group.length() *
                englishFrequency[plainLetter] / 100.0;

            if(expected > 0)
            {
                double difference =
                    observed[cipherLetter] - expected;

                chiSquare +=
                    (difference * difference) / expected;
            }
        }

        if(chiSquare < bestScore)
        {
            bestScore = chiSquare;
            bestShift = shift;
        }
    }

    return bestShift;
}


// 7. Find complete Vigenere key
string find_key(vector<string> groups)
{
    string key = "";

    cout << "\nShift Analysis\n";
    cout << "--\n";

    for(int i = 0; i < groups.size(); i++)
    {
        int shift = find_shift(groups[i]);

        char keyCharacter =
            'A' + shift;

        key += keyCharacter;

        cout << "Group "
             << i + 1
             << " -> Shift = "
             << shift
             << " -> Key letter = "
             << keyCharacter
             << endl;
    }

    return key;
}


// 8. Vigenere decryption
string vigenere_decrypt(string ciphertext, string key)
{
    string plaintext = "";

    for(int i = 0; i < ciphertext.length(); i++)
    {
        int c = ciphertext[i] - 'A';

        int k =
            key[i % key.length()] - 'A';

        int p =
            (c - k + 26) % 26;

        plaintext += char('A' + p);
    }

    return plaintext;
}


// 9. Vigenere encryption
string vigenere_encrypt(string plaintext, string key)
{
    string ciphertext = "";

    for(int i = 0; i < plaintext.length(); i++)
    {
        int p = plaintext[i] - 'A';

        int k =
            key[i % key.length()] - 'A';

        int c =
            (p + k) % 26;

        ciphertext += char('A' + c);
    }

    return ciphertext;
}


// 10. Verification
bool verify(string plaintext,
            string originalCiphertext,
            string key)
{
    string encrypted =
        vigenere_encrypt(plaintext, key);

    return encrypted == originalCiphertext;
}


int main()
{
    string ciphertext = R"(

DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA
MKTTF TCCFX
KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP
WFKLS LEASE
PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW
NUOVJ MJCLL
OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ
ZVRMN WTQSE
OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM
OECBX SESCI
YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL
RYELH QSVWB
AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV
OVVXH KWQIL
IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE
TZEDF

)";

    // Step 1
    string cleaned =
        clean_ciphertext(ciphertext);

    cout << "CLEANED CIPHERTEXT\n";
    cout << "===\n";

    cout << cleaned << endl;

    cout << "\nTotal characters = "
         << cleaned.length()
         << endl;


    // Step 2
    int keyLength =
        kasiski_analysis(cleaned);

    cout << "\n=\n";

    cout << "Estimated Key Length = "
         << keyLength
         << endl;


    // Step 3
    vector<string> groups =
        split_into_groups(cleaned,
                          keyLength);


    // Step 4
    cout << "\nFREQUENCY ANALYSIS\n";
    cout << "\n";

    frequency_analysis(groups);


    // Step 5
    string key =
        find_key(groups);

    cout << "\nRecovered Key = "
         << key
         << endl;


    // Step 6
    string plaintext =
        vigenere_decrypt(cleaned,
                         key);

    cout << "\nRECOVERED PLAINTEXT\n";
    cout << "\n";

    cout << plaintext << endl;


    // Step 7 and 8
    cout << "\nVERIFICATION\n";
    cout << "\n";

    if(verify(plaintext,
              cleaned,
              key))
    {
        cout << "SUCCESS" << endl;
        cout << "Re-encrypted plaintext matches "
             << "the original ciphertext."
             << endl;
    }
    else
    {
        cout << "FAILED" << endl;
    }

    return 0;
}