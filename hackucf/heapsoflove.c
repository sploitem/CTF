#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "pwnable_harness.h"



static const char* flagfile = "flag.txt";
static void giveFlag(void) {
	char flag[64];
	FILE* fp = fopen(flagfile, "r");
	if(!fp) {
		perror(flagfile);
		return;
	}
	
	fgets(flag, sizeof(flag), fp);
	fclose(fp);
	puts(flag);
}


typedef struct user_account {
	char* name;
	int fingers;
	int gender;
} user_account;


void* fmalloc(size_t size) {
	void* ptr = malloc(size);
	if(!ptr) {
		exit(EXIT_FAILURE);
	}
	return ptr;
}

void read_line(char* buf, size_t bufsize) {
	if(read(STDIN_FILENO, buf, bufsize) == -1) {
		exit(EXIT_FAILURE);
	}
	buf[bufsize-1] = '\0';
	
	char* end = strchr(buf, '\n');
	if(end) {
		*end = '\0';
	}
}


void display_gender(user_account* user) {
	switch(user->gender) {
		case 1:
			printf("Male\n");
			break;
		
		case 2:
			printf("Female\n");
			break;
		
		case 3:
			printf("Boat\n");
			break;
		
		case 4:
			printf("Apache attack helicopter\n");
			break;
		
		case 5:
			printf("Gender fluid\n");
			break;
		
		case 6:
			printf("Tumblr user\n");
			break;
		
		case 7:
			printf("Also a tumblr user\n");
			break;
		
		case 8:
			printf("Some made-up gender\n");
			break;
		
		case 1337:
			if(user->fingers != 10) {
				printf("You almost tricked us into thinking you were a hacker.\n");
				printf("However, everyone knows that hackers have all 10 fingers.\n");
				printf("You happen to have %d fingers, not 10.\n", user->fingers);
				printf("Otherwise, how could they type on keyboards while wearing ski masks?\n");
				break;
			}
			
			printf("Wow, you're actually a hacker!\n");
			printf("We found a match for you: ");
			giveFlag();
			printf("We hope you and your match get along well!\n");
			exit(EXIT_SUCCESS);
		
		default:
			printf("Unknown gender #%d, how peculiar.\n", user->gender);
			printf("We bet you think you're quite fabulous.\n");
			break;
	}
}

int ask_fingers(void) {
	printf("\n");
	printf("How many fingers do you have, oh disfigured one?\n");
	printf("\n");
	printf("Fingers: ");
	
	char fingers_str[5];
	read_line(fingers_str, sizeof(fingers_str));
	
	int fingers;
	while(sscanf(fingers_str, "%d", &fingers) != 1 || fingers == 10) {
		if(fingers == 10) {
			printf("Come on, we know you either have too many or not enough fingers.\n");
		}
		
		printf("Invalid choice (%s). Please enter a number that's not 10.\n", fingers_str);
		printf("\n");
		printf("Fingers: ");
		read_line(fingers_str, sizeof(fingers_str));
	}
	
	return fingers;
}

int ask_gender(void) {
	printf("\n");
	printf("What is your gender, oh beautiful one?\n");
	printf("[1] Male\n");
	printf("[2] Female\n");
	printf("[3] Boat\n");
	printf("[4] Apache attack helicopter\n");
	printf("[5] Gender fluid\n");
	printf("[6] Excuse me, did you just assume my gender? (tumblr user)\n");
	printf("[7] All of the above\n");
	printf("[8] Other/prefer not to answer\n");
	printf("[1337] Hacker\n");
	printf("\n");
	printf("Gender: ");
	
	char choice_str[5];
	read_line(choice_str, sizeof(choice_str));
	
	int choice;
	while(sscanf(choice_str, "%d", &choice) != 1 || choice < 1 || 8 < choice) {
		if(choice == 1337) {
			printf("We're sorry, but you're clearly not a hacker.\n");
			printf("If you really think you're a hacker, prove it.\n");
		}
		printf("Invalid choice (%s). Please enter a number 1-8.\n", choice_str);
		printf("\n");
		printf("Gender: ");
		read_line(choice_str, sizeof(choice_str));
	}
	
	return choice;
}

user_account* make_user(char* name) {
	user_account* user = fmalloc(sizeof(*user));
	user->name = name;
	return user;
}

int menu(user_account* user) {
	printf("\n");
	printf("What do you wish to do, oh intelligent one?\n");
	printf("[1] Search for matching dates\n");
	printf("[2] Change name\n");
	printf("[3] Change gender\n");
	printf("[4] I found a date!!!\n");
	printf("[5] Log out\n");
	printf("\n");
	printf("Choice: ");
	
	char choice_str[5];
	read_line(choice_str, sizeof(choice_str));
	
	int choice;
	while(sscanf(choice_str, "%d", &choice) != 1 || choice < 1 || 5 < choice) {
		printf("Invalid choice (%s). Please type a number 1-5\n", choice_str);
		printf("\n");
		printf("Choice: ");
		read_line(choice_str, sizeof(choice_str));
	}
	
	return choice;
}

void handle_connection(int sock) {
	printf("Welcome to Heaps of Love, a new secure online dating service!\n");
	printf("What is your name, oh lovely lonely one?\n");
	printf("\n");
	printf("Name: ");
	
	char name[100];
	read_line(name, 100);
	printf("\n");
	
	user_account* user = make_user(strdup(name));
	user->fingers = ask_fingers();
	user->gender = ask_gender();
	
	while(true) {
		int choice = menu(user);
		switch(choice) {
			case 1:
				printf("We're sorry, it appears that nobody on this planet wants to date you.\n");
				break;
			
			case 2:
				printf("What is your new name, oh breathtaking one?\n");
				read_line(user->name, 100);
				break;
			
			case 3:
				printf("Your gender is currently set to: ");
				display_gender(user);
				user->gender = ask_gender();
				break;
			
			case 4:
				printf("Yeah right.\n");
				break;
			
			case 5:
				printf("You have successfully logged out!\n");
				return;
		}
	}
}



/* Everything below can safely be ignored and is not part of the challenge. */
int main(int argc, char** argv) {
	server_options opts = {
		.user = "heapsoflove",
		.chrooted = true,
		.port = 7001,
		.time_limit_seconds = 30
	};
	
	return server_main(argc, argv, opts, &handle_connection);
}
