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

int compare(const void *a, const void *b) {
    return ((Profissionais *)a)->id - ((Profissionais *)b)->id;
}

void listProf(Profissionais prof[], int count) {
    printf("Lista de profissionais:\n");
    printf("\n");
    for (int i = 0; i < count; i++) {
        if (prof[i].active) {
            printf("ID: %d | Nome: %s | Especializacao: %s\n", prof[i].id, prof[i].nome, prof[i].especializacao);
        }
    }
}

void addProf(Profissionais prof[], int *count, char *nome, char *especializacao, int *profId) {
    Profissionais newProf;
    newProf.id = rand() % 1000 + 1;
    *profId = newProf.id;
    strcpy(newProf.nome, nome);
    strcpy(newProf.especializacao, especializacao);
    newProf.active = 1;
    prof[*count] = newProf;
    (*count)++;
    printf("Profissional adicionado com sucesso.\n");
}

void addProf_sorted(Profissionais prof[], int *count, char *nome, char* especializacao, int *prof_id) {
    Profissionais new_prof;
    new_prof.id = rand() % 1000 + 1;
    *prof_id = new_prof.id;
    strcpy(new_prof.nome, nome);
    strcpy(new_prof.especializacao, especializacao);
    new_prof.active = 1;
    int i;
    for (i = *count - 1; (i >= 0 && prof[i].id > new_prof.id); i--) {
        prof[i + 1] = prof[i];
    }
    prof[i + 1] = new_prof;
    (*count)++;

    FILE *file = fopen("sorted_file.bin", "wb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    fwrite(prof, sizeof(Profissionais), *count, file);
    fclose(file);

    printf("Profissional adicionado com sucesso.\n");
}

void addProf_heap(Profissionais prof[], int *count, char *nome, char* especializacao, int *prof_id) {
    Profissionais new_prof;
    new_prof.id = rand() % 1000 + 1;
    *prof_id = new_prof.id;
    strcpy(new_prof.nome, nome);
    strcpy(new_prof.especializacao, especializacao);
    new_prof.active = 1;
    prof[*count] = new_prof;
    (*count)++;
    int i = *count - 1;
    while (i != 0 && prof[(i - 1) / 2].id < prof[i].id) {
        Profissionais temp = prof[(i - 1) / 2];
        prof[(i - 1) / 2] = prof[i];
        prof[i] = temp;
        i = (i - 1) / 2;
    }
    FILE *file = fopen("heap_file.bin", "wb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    fwrite(prof, sizeof(Profissionais), *count, file);
    fclose(file);

    printf("Profissional adicionado com sucesso.\n");
}
void readProf(Profissionais prof[], int count, int profId) {
    for (int i = 0; i < count; i++) {
        if (prof[i].id == profId && prof[i].active) {
            printf("ID: %d | Nome: %s | Especializacao: %s\n", prof[i].id, prof[i].nome, prof[i].especializacao);
            return;
        }
    }
    printf("Profissional com a ID %d nao encontrado.\n", profId);
}

void updateProf(Profissionais prof[], int count, int profId, char *novoNome, char *novaEspec) {
    for (int i = 0; i < count; i++) {
        if (prof[i].id == profId && prof[i].active) {
            strcpy(prof[i].nome, novoNome);
            strcpy(prof[i].especializacao, novaEspec);
            printf("\n");
            printf("Profissional atualizado com sucesso.\n");
            return;
        }
    }
    printf("Profissional com a ID %d nao encontrado.\n", profId);
}

void deleteProf(Profissionais prof[], int *count, int profId) {
    for (int i = 0; i < *count; i++) {
        if (prof[i].id == profId && prof[i].active) {
            prof[i].active = 0;
            printf("Profissional deletado com sucesso.\n");
            return;
        }
    }
    printf("Profissional com ID %d nao encontrado.\n", profId);
}

void saveProfBinary(Profissionais prof[], int count, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    fwrite(prof, sizeof(Profissionais), count, file);
    fclose(file);
}

void loadProfBinary(Profissionais prof[], int *count, const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    *count = fread(prof, sizeof(Profissionais), MAX_TASKS, file);
    fclose(file);
}

void removeInactive(Profissionais prof[], int *count) {
    int j = 0;
    for (int i = 0; i < *count; i++) {
        if (prof[i].active) {
        prof[j++] = prof[i];
        }
    }
    *count = j;

    FILE *file = fopen("normal_file.bin", "wb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    fwrite(prof, sizeof(Profissionais), *count, file);
    fclose(file);

    printf("Profissionais inativos removidos com sucesso.\n");
}

int main() {
    srand(time(NULL));
    Profissionais normal_prof[MAX_TASKS];
    Profissionais sorted_prof[MAX_TASKS];
    Profissionais heap_prof[MAX_TASKS];
    int count_normal = 0, count_sorted = 0, count_heap = 0;
    int profId1, profId2, profId3;   
    clock_t start, end;
    
    // NORMAL
    start = clock();
    removeInactive(normal_prof, &count_normal);
    addProf(normal_prof, &count_normal, "João Silva", "Cardiologista", &profId1);
    addProf(normal_prof, &count_normal, "Maria Santos", "Pediatra", &profId2);
    addProf(normal_prof, &count_normal, "Claudio Pereira", "Dermatologista", &profId3);
    end = clock();
    printf("Tempo para adicionar profissionais (Normal File): %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    listProf(normal_prof, count_normal);

    // SORTED
    start = clock();
    removeInactive(sorted_prof, &count_sorted);
    addProf_sorted(sorted_prof, &count_sorted, "João Silva", "Cardiologista", &profId1);
    addProf_sorted(sorted_prof, &count_sorted, "Maria Santos", "Pediatra", &profId2);
    addProf_sorted(sorted_prof, &count_sorted, "Claudio Pereira", "Dermatologista", &profId3);
    end = clock();
    printf("Tempo para adicionar profissionais (Sorted File): %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    listProf(sorted_prof, count_sorted);

    // HEAP

    start = clock();
    removeInactive(heap_prof, &count_heap);
    addProf_heap(heap_prof, &count_heap, "João Silva", "Cardiologista", &profId1);
    addProf_heap(heap_prof, &count_heap, "Maria Santos", "Pediatra", &profId2);
    addProf_heap(heap_prof, &count_heap, "Claudio Pereira", "Dermatologista", &profId3);
    end = clock();
    printf("Tempo para adicionar profissionais (Heap File): %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    listProf(heap_prof, count_heap);
    return 0;
}
