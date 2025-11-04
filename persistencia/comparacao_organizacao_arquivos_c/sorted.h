#ifndef SORTED_H
#define SORTED_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TASKS 100

typedef struct {
    int id;
    char nome[50];
    char especializacao[50];
    int active; // flag for active/inactive
} Profissionais;

void addProf_sorted(Profissionais prof[], int *count, char *nome, char* especializacao, int *prof_id);

#endif