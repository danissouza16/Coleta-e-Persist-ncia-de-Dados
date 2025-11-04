#ifndef NORMAL_H
#define NORMAL_H

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

void listProf(Profissionais prof[], int count);
void addProf(Profissionais prof[], int *count, char *nome, char *especializacao, int *profId);
void readProf(Profissionais prof[], int count, int profId);
void updateProf(Profissionais prof[], int count, int profId, char *novoNome, char *novaEspec);
void deleteProf(Profissionais prof[], int *count, int profId);
void saveProfBinary(Profissionais prof[], int count, const char *filename);
void loadProfBinary(Profissionais prof[], int *count, const char *filename);
void removeInactive(Profissionais prof[], int *count);
void clearProfTXT(const char *filename);
void clearProfBinary(const char *filename);

#endif