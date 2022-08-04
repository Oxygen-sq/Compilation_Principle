#include <cstdlib>
#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;

char a[100];
string b[100];
static int j = 0;
static int p = 0;
int k = 0;
int count;
int indexs = 0;
int m, n;
void E();
void E1(); // X->+TX|-TX
void T();
void T1(); // Y->*FY|/FY
void F();  // F->(E) | i
bool isnum();
bool isid();
void error();
void Rank();

int main() {
    char c;
    m = -1, n = -1;
    cout << "������ʽ��";
    c = getchar();
    while (c != '\n') {
        a[k] = c;
        k++;
        c = getchar();
    }
    k++;
    a[k] = '#';
    for (int i = 0; i <= k;
         i++) //��ʼ��������a[]���ַ�ʶ��ȥ���ո��,�жϱ��ʽ�����Ƿ�Ϸ�
    {
        switch (a[i]) {

        case ' ':
            break;

        case '\0':
            break;

        case '\n':
            break;

        case '\t':
            break;

        case '+': {
            b[j] += a[i];
            j++;
        }; break;

        case '-': {
            b[j] += a[i];
            j++;
        }; break;

        case '*': {
            b[j] += a[i];
            j++;
        }; break;

        case '/': {
            b[j] += a[i];
            j++;
        }; break;

        case '(': //ʶ����ţ�
        {
            b[j] = a[i];
            j++;
        }; break;

        case ')': //ʶ����ţ�
        {
            b[j] = a[i];
            j++;
        }; break;

        case '#': //ʶ����ţ�
        {
            b[j] = a[i];
            j++;
        }; break;

        default: {
            if (a[i] >= 'a' && a[i] <= 'z') //ʶ���ʶ��
            {
                b[j] += a[i];
                if (a[i + 1] < 'a' || a[i + 1] > 'z') {
                    j++;
                }
            }

            else if (a[i] >= '0' && a[i] <= '9') //ʶ������
            {
                b[j] += a[i];

                if (a[i + 1] < '0' || a[i + 1] > '9') {
                    j++;
                }
            }

            else {
                cout << "������ʽ���Ϸ���";
                return 0;
            }
        }; break;
        }
    }

    for (int i = 0; i < j; i++) {
        cout << b[i];
    }

    cout << endl;

    cout << "����\t �ķ�\t\t ������\t\t\t�����ַ�\t\tʣ�മ\n";

    E();

    // if (p + 1 == j) {
    if (b[indexs] == "#") {
        cout << "��ȷ��䣡" << endl;
    } else {
        cout << "������䣡" << endl;
    }

    return 0;
}

// �ж��Ƿ�Ϊ���� isdigit(s[i]
bool isnum(string s) {
    int len = s.length();
    for (int i = 0; i < len; i++) {
        if (!isdigit(s[i])) {
            return false;
        }
    }
    return true;
}

// ִ�в����¼
void Rank() {
    cout << count << '\t';
    count++;
}

// �ж��Ƿ�ΪӢ����ĸ isalpha(s[i])
bool isid(string s) {
    int len = s.length();
    for (int i = 0; i < len; i++) {
        if (!isalpha(s[i])) {
            return false;
        }
    }
    return true;
}

void error() {
    cout << "����!" << endl;
    exit(0);
}

// �����ǰ������
void analyze() {
    if (m < 0)
        cout << ' ';
    else {
        for (int i = 0; i <= m; i++)
            cout << b[i];
    }
    cout << '\t' << '\t' << '\t';
}

// �����ǰ�����ַ�
void latter() {
    cout << b[indexs];
    cout << '\t' << '\t' << '\t';
}

// ���ʣ������ַ�
void remain() {
    for (int j = n + 1; j <= k; j++)
        cout << b[j];
    cout << endl;
}

void E() {
    T();
    E1();
}

void E1() {
    if (b[p] == "+") {
        Rank();
        p++;
        cout << "X ->+TX\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
        T();
        E1();
    } else if (b[p] == "-") {
        Rank();
        p++;
        cout << "X ->-TX\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
        T();
        E1();
    }
}

void T() {
    F();
    T1();
}

void T1() {
    if (b[p] == "*") {
        Rank();
        p++;
        cout << "Y ->*FY\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
        F();
        T1();
    } else if (b[p] == "/") {
        Rank();
        p++;
        cout << "Y ->/FY\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
        F();
        T1();
    }
}

void F() {
    if (isid(b[p])) {
        Rank();
        p++;
        cout << "F ->i\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
    } else if (isnum(b[p])) {
        Rank();
        p++;
        cout << "F ->i\t\t";
        m++;
        n++;
        analyze();
        latter();
        remain();
        indexs++;
    } else {
        if (b[p] == "(") {
            Rank();
            p++;
            cout << "F ->(E)\t\t";
            m++;
            n++;
            analyze();
            latter();
            remain();
            indexs++;
            E();
            if (b[p] == ")") {
                Rank();
                p++;
                cout << "F ->(E)\t\t";
                m++;
                n++;
                analyze();
                latter();
                remain();
                indexs++;
            } else {
                error();
            }
        } else {
            error();
        }
    }
}

