/*
ECE 370
Banking Application Project
by Yuuki Nishida
*/
#include <iostream>
using namespace std;
struct CustomerAccount
{
    string name;
    int accountNumber;
    float balance;
    string accountType;
};
struct CustomerRequest
{
    string name;
    int accountNumber;
    float amount;
    string requestType;
};
//************************************************************************************
class QNode
{
public:
    CustomerRequest requests;
    QNode* next;
    QNode()
    {
        requests.name="";
        requests.accountNumber=0;
        requests.amount=0;
        requests.requestType="";
        next=NULL;
    }
};
class RequestQueue
{
public:
    QNode* front;
    QNode* rear;
//-------------------------------------------------------------------------------------------
    RequestQueue()
    {
        front=NULL;
        rear=NULL;
    }
//-------------------------------------------------------------------------------------------
    bool isEmpty()
    {
        if(front==NULL)
            return true;
        else
            return false;
    }
    CustomerRequest getFront()
    {
        return front->requests;
    }
//-------------------------------------------------------------------------------------------
    void Enqueue(CustomerRequest customer)
    {
        QNode* newNode=new QNode();
        newNode->requests=customer;
        if(isEmpty())
            front=rear=newNode;
        else
        {
            rear->next=newNode;
            rear=newNode;
        }
    }
//-------------------------------------------------------------------------------------------
    CustomerRequest dequeue()
    {
        CustomerRequest customer;
        if(isEmpty())
            cout << " The queue is empty \n";
        else if(front==rear)
        {
            customer = front->requests;
            delete front;
            front=rear=NULL;
        }
        else
        {
            QNode* delptr=front;
            customer=front->requests;
            front=front->next;
            delete delptr;
        }
        return customer;
    }
    void display()
    {
        QNode*temp=front;
        cout <<"Name of Account Holder: "<<temp->requests.name<<endl;
        cout <<"Account Number: "<<temp->requests.accountNumber<<endl;
        cout <<"Request type: "<<temp->requests.requestType<<"\t"<<"Transaction to Account: "<<temp->requests.amount;
    }
};
//************************************************************************************
class BSTNode
{
public:
    CustomerAccount account;
    BSTNode* left;
    BSTNode* right;
    BSTNode(CustomerAccount customer)
    {
        account=customer;
        left=NULL;
        right=NULL;
    }
};
class AccountTree
{
public:
    BSTNode*root;
    AccountTree()
    {
        root=NULL;
    }
    BSTNode* Insert(BSTNode* r, CustomerAccount customer)
    {
        if(r==NULL)
        {
            BSTNode* newnode=new BSTNode(customer);
            r=newnode;
        }
        else if(customer.accountNumber<r->account.accountNumber)
            r->left=Insert(r->left, customer);
        else
            r->right=Insert(r->right, customer);
        return r;
    }
    BSTNode*Delete(BSTNode*r, CustomerAccount customer)
    {
        if(r==NULL)
            return NULL;
        if(customer.accountNumber<r->account.accountNumber)
            r->left=Delete(r->left, customer);
        else if(customer.accountNumber>r->account.accountNumber)
            r->right=Delete(r->right, customer);
        else
        {
            if(r->left==NULL && r->right==NULL)
                r=NULL;
            else if(r->left!=NULL&&r->right==NULL)
            {
                r->account=r->left->account;
                delete r->left;
                r->left=NULL;
            }
            else if(r->left==NULL&&r->right!=NULL)
            {
                r->account=r->right->account;
                delete r->right;
                r->right=NULL;
            }
            else
            {
                BSTNode*min=Findmin(r->right);
                r->account=min->account;
                r->right=Delete(r->right, min->account);
            }
        }
        return r;
    }
    BSTNode*Search(BSTNode*r, CustomerAccount customer)
    {
        if(r==NULL)
            return NULL;
        else if(r->account.accountNumber==customer.accountNumber)
            return r;
        else if(customer.accountNumber <r->account.accountNumber)
            return Search(r->left, customer);
        else
            return Search(r->right, customer);
    }
    bool Search(CustomerAccount customer)
    {
        BSTNode* result=Search(root, customer);
        if(result==NULL)
            return false;
        else
            return true;
    }
    void displayAccount(CustomerAccount customer)
    {
        BSTNode* display=Search(root, customer);
        cout<<"Name"<<"\t\t"<<"AccountNumber"<<"\t\t"<<"Account type"<<"\t\t"<<"Balance"<<endl;
        cout<<"----------------------------------------------------------------------------"<<endl;
        cout<<display->account.name<<"\t\t"<<display->account.accountNumber<<"\t\t"<<display->account.accountType<<"\t\t"<<"$"<<display->account.balance<<endl;
    }
    BSTNode*Findmin(BSTNode*r)
    {
        if(r==NULL)
            return NULL;
        else if(r->left==NULL)
            return r;
        else 
            return Findmin(r->left);
    }
    void Inorder(BSTNode*r)
    {
        if(r==NULL)
            return;
        Inorder(r->left);
        cout<<r->account.name<<"\t"<<r->account.accountNumber<<"\t"<<r->account.accountType<<"\t"<<"$"<<r->account.balance<<endl;
        Inorder(r->right);
    }
    void Insert(CustomerAccount data)
    {
        root=Insert(root, data);
    }
};
//************************************************************************************
int main()
{
    RequestQueue requests;
    AccountTree Account;
    int assign = 56704500;
    int choice;
    while(1)
    {
        cout <<endl;
        cout <<"    Banking Management System"<<endl;
        cout <<"---------------------------------"<<endl;
        cout <<"1. Create Account"<<endl;
        cout <<"2. Delete Account"<<endl;
        cout <<"3. Search Account"<<endl;
        cout <<"4. Account Transaction"<<endl;
        cout <<"5. Display Account Information"<<endl;
        cout <<"6. Exit\n";
        cout <<"Enter your choice (1-6): ";
        cin >> choice;
        cout <<endl;
        //Create Account
        if(choice==1)
        {
            CustomerRequest newAccount;
            bool isValidName;
            do {
                isValidName = true;
                cout <<"Enter Name of Account holder: ";
                cin >>newAccount.name;
                
                for(int i=0;i<newAccount.name.length();++i)
                {
                    if(!isalpha(newAccount.name[i]))
                    {
                        isValidName = false;
                        cout << "Invalid name. Name must contain only alphabetic characters.\n";
                        break;
                    }
                }
            }
            while(!isValidName);
            newAccount.accountNumber=assign;
            assign++;
            cout <<"Enter initial balance: ";
            cin>>newAccount.amount;
            cout <<"Enter account type (Checking or Savings): ";
            cin >>newAccount.requestType;
            requests.Enqueue(newAccount);
            cout <<"Request added to queue.\n";
        }
        //Delete Account
        else if(choice==2)
        {
            CustomerRequest delRequest;
            cout <<"Enter account number to delete: ";
            cin >>delRequest.accountNumber;
            delRequest.requestType="Delete";
            requests.Enqueue(delRequest);
            cout <<"Request added to queue.\n";
        }
        //Search Account
        else if(choice==3)
        {
            CustomerRequest searchRequest;
            cout <<"Enter account number to search: ";
            cin >>searchRequest.accountNumber;
            searchRequest.requestType="Search";
            requests.Enqueue(searchRequest);
            cout <<"Request added to queue.\n";
        }
        //Access Account
        else if(choice==4)
        {
            CustomerRequest request;
            cout <<"Enter account number: ";
            cin >>request.accountNumber;
            cout <<"Enter transaction amount: ";
            cin >> request.amount;
            cout <<"Enter request type (deposit or withdraw): ";
            cin >>request.requestType;
            requests.Enqueue(request);
            cout <<"Request added to queue.\n";
        }
        //Display All Accounts information
        else if(choice==5)
        {
            CustomerRequest display;
            display.requestType="display";
            requests.Enqueue(display);
            cout <<"Request added to queue.\n";
        }
        while(!requests.isEmpty())
        {
            CustomerRequest process= requests.dequeue();
            CustomerAccount account;
            if(process.requestType=="Checking")
            {
                account.name=process.name;
                account.accountType=process.requestType;
                account.balance=process.amount;
                account.accountNumber=process.accountNumber;
                Account.Insert(account);
                cout <<"Account created successfully. \n\n";
                continue;
            }
            else if(process.requestType=="Savings")
            {
                account.name=process.name;
                account.accountType=process.requestType;
                account.balance=process.amount;
                account.accountNumber=process.accountNumber;
                Account.Insert(account);
                cout <<"Account created successfully. \n\n";
                continue;
            }
            account.accountNumber=process.accountNumber;
            
            BSTNode* accountNode = Account.Search(Account.root, CustomerAccount{process.name, process.accountNumber, 0, ""});
            if(accountNode==NULL && process.requestType!="display")
            {
                cout <<"Account not found for request: "<<process.name<<endl;
                continue;
            }
            else if(process.requestType=="Delete")
            {
                Account.root=Account.Delete(Account.root, account);
                cout<<"Account deleted successfully.\n";
            }
            else if(process.requestType=="Search")
                Account.displayAccount(accountNode->account);   
            else if(process.requestType=="deposit")
                accountNode->account.balance+=process.amount;
            else if(process.requestType=="withdraw")
            {
                if(accountNode->account.balance<process.amount)
                {
                    cout <<"Insufficient balance for request: " << process.name<<endl;
                    continue;
                }
                accountNode->account.balance-=process.amount;
            }
            else if(process.requestType=="display")
            {
                cout<<"Name"<<"\t"<<"AccountNumber"<<"\t"<<"Account type"<<"\t"<<"Balance"<<endl;
                cout<<"----------------------------------------------------------------------------"<<endl;
                Account.Inorder(Account.root);
            }
            else
            {
                cout << "Invalid requesttype for request"<<process.name<<endl;
            }
        }
    }
}