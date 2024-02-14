#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
#include<string.h>
// ------------------------------------------
void delPRODUCT();
void modify();
int display();
void buy();
int search(int);
int check(int);
int value=0;

// ------------------------------------------
struct node {
    int ID;
    char pName[100];
    double pPrice;
    int qnty;
    struct node* next;
};
struct node *head=NULL;
void start(){
    system("cls");
    int id,quant; //quant = quantity
    char name[100];
    double proP;  //price
    struct node *t = (struct node*) malloc(sizeof(struct node));

    printf("\t\t\tEnter product ID -->");
    scanf("%d",&id);
    t->ID=id;
    printf("\t\t\tEnter product Name -->");
    scanf("%s",&name);
    for(int i = 0;i<100;i++){
        t->pName[i]=name[i];
    }
    printf("\t\t\tEnter product price -->");
    scanf("%lf",&proP);
    t->pPrice=proP;
    printf("\t\t\tEnter product quantity -->");
    scanf("%d",&quant);
    t->qnty=quant;
    t->next= head;
    head = t;
    system("cls");
    printf("\n\n\t\tThis Product is Added!\n\n\n");
}

void end(){
    system("cls");
    int id,quant; //quant = quantity
    char name[100];
    double proP;  //price
    struct node *t = (struct node*) malloc(sizeof(struct node));
    struct node *r=head;
    printf("\t\t\tEnter product ID -->");
    scanf("%d",&id);
    t->ID=id;
    printf("\t\t\tEnter product Name -->");
    scanf("%s",&name);
    for(int i = 0;i<100;i++){
        t->pName[i]=name[i];
    }
    printf("\t\t\tEnter product price -->");
    scanf("%lf",&proP);
    t->pPrice=proP;
    printf("\t\t\tEnter product quantity -->");
    scanf("%d",&quant);
    t->qnty=quant;

    while (r->next!=NULL){
        r=r->next;
    }
    r->next = t;
    r->next = NULL;
    system("cls");
    printf("\n\n\t\tThis Product is Added!\n\n\n");
}

int display(){
    system("cls");
    int c = 0;
    struct node *r=head;
    printf("Products that are available --> \n");
    printf("ID\t\t\tProduct Name\t\t\tPrice\t\t\tQuantity\n");
    while (r!=NULL){
        printf("%d\t\t\t%s\t\t\t%lf\t",r->ID,r->pName,r->pPrice);
        if(check(r->qnty)<=0)
            printf("Out of Stock!\n");
        else
            printf("%d\n",check(r->qnty));
        r=r->next;
        c=c+1;
    }
    printf("\n\nTotal products in our market is =>%d\n\n\n",c);
    return c;
}

int check(int quant){
    int a = quant;
    if(quant<=0)
        return 0;
    else{
        return quant;
    }
}

int search(int id){
    int count = 1;
    struct node *r=head;
    while (r!=NULL){
        if(r->ID==id)
            break;
        else
            count++;
        r=r->next;
    }
    return count;
}

// ---------------------------------------------------------

int main(){

    int f1,f2;
    printf("*************************************************************************************\n");
    printf("********************************    Isekai Market    ********************************\n");
    printf("*************************************************************************************\n\n");
    int temp = 1;
    while (1)
    {
        int key;
        f1=1;
        f2=1;
        printf("\t\t\t\tEnter 1 for Staff portal\n\n\t\t\t\tEnter 2 for Customer Portal\n\n\t\t\t\tEnter 0 to Exit!\n\n");
        printf("*************************************************************************************\n");
        printf("*************************************************************************************\n\n");
        printf("\t\t\t=> ");
        scanf("%d",&key);
        printf("\n");
        switch (key)
        {
            case 1:
                while (f1)
                {
                    int ch;
                    printf("\t\t\tEnter 1 to Insert a new product\n\n\t\t\tEnter 2 to Display all products\n\n\t\t\tEnter 3 to Modify existing product\n\n");
                    printf("\t\t\tEnter 4 to Delete a particular product item\n\n\t\t\tEnter 0 to Exit!\n\n");
                    printf("*************************************************************************************\n");
                    printf("\t\t=> ");
                    scanf("%d",&key);
                    switch (key)
                    {
                        case 1:
                            if(temp==0){
                                end();
                            }
                            if(temp==1){
                                value++;
                                start();
                                temp=0;
                            }
                            break;
                        case 2:
                            system("cls");
                            display();
                            break;
                        case 3:
                            modify();
                            break;
                        case 4:
                            delPRODUCT();
                            break;
                        case 0:
                            printf("Exiting 3 2 1....\n");
                            f1=0;
                            break;
                        default:
                            system("cls");
                            printf("\t\t\t      this choice does not exist!      \n\n");
                            break;
                    }
                }
                break;
            case 2:
                while (f2)
                {
                    int key2;
                    printf("\t\t\tEnter 1 to buy something :v\n\n\t\t\tEnter 2 to Exit\n\n");
                    printf("*************************************************************************************\n");
                    printf("\t\t\t=> ");
                    scanf("%d",&key2);
                    printf("\n\n");
                    switch (key2)
                    {
                        case 1:
                            buy();
                            break;
                        case 2:
                            printf("Exiting 3 2 1....\n");
                            f2=0;
                            break;
                        default:
                            system("cls");
                            printf("\t\t\t      this choice does not exist!      \n\n");
                            break;
                    }
                }
                break;
            case 0:
                printf("Exiting 3 2 1....\n");
                exit(1);
                break;
            default:
                system("cls");
                printf("\t\t\t      this choice does not exist!      \n\n");
                break;
        }
    }

    // char choice;

    // system("cls");
    // printf("\n\n\n\n\n\n\n\n\n**************************************************************");
    // printf("\n\t\t------WELCOME TO THE TELECOM BILLING MANAGEMENT SYSTEM---");
    // printf("\n\t\t****************************************************************");
    // Sleep(2000);
    // getch();
    // system("cls");
    // while (1)
    // {
    // 	system("cls");
    // 	printf("\n Enter\n A : Add new record.\n L : list of records");
    // 	printf("\n M : Modify record.\n P : for payment");
    // 	printf("\n S : Search record.");
    // 	printf("\n D : Delete record.\n E : for exit\n");
    // 	choice=getche();
    // 	choice=toupper(choice);
    // 	switch(choice)
    // 	{
    // 		case 'P':
    // 			payment();break;
    // 		case 'A':
    // 			addrecords();break;
    // 		case 'L':
    // 			listrecords();break;
    // 		case 'M':
    // 			modifyrecords();break;
    // 		case 'S':
    // 			searchrecords();break;
    // 		case 'D':
    // 			deleterecords();break;
    // 		case 'E':
    // 			system("cls");
    // 			printf("\n\n\t\t\t\tTHANK YOU");
    // 			exit(0);
    // 			break;
    // 		default:
    // 			system("cls");
    // 			printf("Incorrect Input");
    // 			printf("\nAny key to continue");
    // 			getch();
    // 	}
    // }
}

void delPRODUCT(){
    system("cls");
    display();
    int id;
    struct node *current = head;
    struct node *pre = head;
    printf("\n\nEnter ID to delete that product -->\n\n");
    scanf("%d",&id);
    if(head == NULL){
        system("cls");
        printf("List is empty\n");
    }
    int pos = 0;
    int count = display();
    pos = search(id);
    if(pos<=count){
        while(current->ID!=id){
            pre = current;
            current = current->next;
        }
        pre->next = current->next;
        system("cls");
        printf("\n\nItem is deleted!\n\n");
    }
    else
        printf("\nNot Found!\n");
}

void modify(){
    int id;
    double pre;
    char proName[100];
    if(head == NULL){
        system("cls");
        printf("List is empty\n");
    }
    else{
        printf("\n\nEnter the ID to change product Name and its Price\n");
        scanf("%d",&id);
        struct node * current=head;
        int pos = 0;
        int count = display();
        pos = search(id);
        if(pos<=count){
            while (current->ID != id)
            {
                current=current->next;
            }
            printf("\nOld Name => ");
            printf("%s", current->pName);
            printf("\nOld Price => ");
            printf("%lf", current->pPrice);

            printf("Enter New Name => ");
            scanf("%s",&proName);
            for(int i=0;i<100;i++){
                current->pName[i]=proName[i];
            }
            printf("Enter new price => ");
            scanf("%lf",&pre);
        }
        else
            printf("%d is Not Found\n\n",id);
    }
}

void buy(){
    system("cls");
    int pay = 0,no,price,id,i=1;
    if(head == NULL)
        printf("\n  There is no item to buy  \n\n");
    else{
        printf("How many item do u want to buy!\n");
        scanf("%d",&no);
        int count=display();
        while (i<=no){
            struct node *current=head;
            int quant;
            printf("Enter id, that u want to buy =>");

            int id, pos=0;
            scanf("%d",&id);
            pos=search(id);
            if(pos<=count){
                while (current->ID != id)
                {
                    current=current->next;
                }
                printf("How many quantities do u want =>");
                scanf("%d",&quant);
                pay=pay+(current->pPrice*quant);
                current->qnty= current->qnty-quant;
                i++;
                printf("\n\n        You have bought => ");
                printf("%s\n\n",current->pName);
            }
            else
                printf("\n      This item is not available in our Market        \n\n");
        }
    }
    price = pay*(0.90);
    printf("\n\n\t\t\t\tOriginal Price => %d\n",pay);
    printf("\t\t\t\t\twith 10 percent discount => %d\n\t\t\t\t\tThank you! pls come again\n\n",price);
}
