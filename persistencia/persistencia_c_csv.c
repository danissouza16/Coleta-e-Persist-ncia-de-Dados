#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TASKS 100

struct profissionais {
    int id;
    char nome[50];
    char especializacao[50];
};

typedef struct profissionais Profissionais;

int binary_search(Profissionais prof[], int tamAtual, int id) {
    int left = 0, right = tamAtual - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (prof[mid].id == id) {
            return mid;
        } else if (prof[mid].id < id) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}


void listProf(Profissionais prof[], int count) {
    printf("Lista de profissionais:\n");
    for (int i = 0; i < count; i++) {
        printf("ID: %d | Nome: %s | Especializacao: %s\n", prof[i].id, prof[i].nome, prof[i].especializacao);
    }
}

void list_one_prof(Profissionais prof[], int tamAtual,int id){
  for (int i = 0; i < tamAtual; i++){
    if (prof[i].id == id){
        printf("%d,%s,%s\n", prof[i].id, prof[i].nome,prof[i].especializacao);
    }
  }
}

void list_one_prof_binary(Profissionais prof[], int tamAtual, int id) {
    int index = binary_search(prof, tamAtual, id);
    if (index != -1) {
        printf("%d,%s,%s\n", prof[index].id, prof[index].nome, prof[index].especializacao);
    } else {
        printf("Profisssional com ID %d não encontrado.\n", id);
    }
}

void readProf(Profissionais prof[], int count, int profId) {
    for (int i = 0; i < count; i++) {
        if (prof[i].id == profId) {
            printf("\n");
            printf("Profissional encontrado:\n");
            printf("ID: %d | Nome: %s | Especializacao: %s\n", prof[i].id, prof[i].nome, prof[i].especializacao);
            return;
        }
    }
    printf("Profissional com a ID %d nao encontrado.\n", profId);
}

void addProf(Profissionais prof[], int *count, char *nome, char *especializacao, int *profId) {
    Profissionais newProf;
    newProf.id = rand() % 1000 + 1; 
    *profId = newProf.id;
    strcpy(newProf.nome, nome);
    strcpy(newProf.especializacao, especializacao);
    prof[*count] = newProf;
    (*count)++;

    printf("Profissional adicionado com sucesso.\n");
    printf("\n");
}

void updateProf(Profissionais prof[], int count, int profId, char *novoNome, char*novaEspec) {
    for (int i = 0; i < count; i++) {
        if (prof[i].id == profId) {
            strcpy(prof[i].nome, novoNome);
            strcpy(prof[i].especializacao, novaEspec);
            printf("Profissional atualizado com sucesso.\n");
            return;
        }
    }
    printf("Profissional com a ID %d nao encontrado.\n", profId);
}

void deleteProf(Profissionais prof[], int *count, int profId) {
    for (int i = 0; i < *count; i++) {
        if (prof[i].id == profId) {
            for (int j = i; j < *count - 1; j++) {
                prof[j] = prof[j + 1];
            }
            (*count)--;
            printf("\n");
            printf("Profissional deletado com sucesso.\n");
            return;
        }
    }
    printf("Profissional com ID %d nao encontrado.\n", profId);
}

void salvaProfTxt(Profissionais prof[], int count) {
    FILE *file = fopen("tasks.txt", "w");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    for (int i = 0; i < count; i++) {
        fprintf(file, "%d,%s,%s\n", prof[i].id, prof[i].nome, prof[i].especializacao);
    }
    fclose(file);
}

void carregaProfDoTxt(Profissionais prof[], int *count) {
    FILE *file = fopen("tasks.txt", "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    while (fscanf(file, "%d,%[^,],%[^,]\n", &prof[*count].id, prof[*count].nome, prof[*count].especializacao) != EOF) {
        (*count)++;
    }
    fclose(file);
}

void salvaProfNoBin(Profissionais prof[], int count) {
    FILE *file = fopen("tasks.bin", "wb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    fwrite(prof, sizeof(Profissionais), count, file);
    fclose(file);
}

void carregaProfDoBin(Profissionais prof[], int *count) {
    FILE *file = fopen("tasks.bin", "rb");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return;
    }
    *count = fread(prof, sizeof(Profissionais), MAX_TASKS, file);
    fclose(file);
}

int main() {
    srand(time(NULL));
    Profissionais prof[MAX_TASKS];
    int count = 0;
    FILE *arq = fopen("tasks.txt", "r");
    int tamAtual = 0;
    if (arq == NULL) {
        printf("Memória insuficiente para abrir o arquivo\n");
        exit(1);
    }

    int i = 0;
    while (fscanf(arq, "%d,%[^,],%[^\n]", &prof[i].id, prof[i].nome, prof[i].especializacao) != EOF) {
        i++;
        tamAtual++;
    }
    fclose(arq);
    clock_t start, end;
    int id1, id2, id3;

    
    start = clock();
    addProf(prof, &count, "Daniel Santana", "Cardiologista", &id1);
    addProf(prof, &count, "João Nascimento", "Dermatologista", &id2);
    addProf(prof, &count, "Thiago Ribeiro", "Pediatra", &id3);
    end = clock();
    printf("Tempo para adicionar profissional: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");
    listProf(prof, count);

    
    start = clock();
    readProf(prof, count, id1);
    end = clock();
    printf("\n");
    printf("Tempo para adicionar profissional: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    
    
    start = clock();
    list_one_prof(prof, count, id1);
    end = clock();
    printf("Tempo para listar o profissional: %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    
    start = clock();
    list_one_prof_binary(prof, count, id1);
    end = clock();
    printf("Tempo para listar o profissional: %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    

    start = clock();
    listProf(prof, count);
    end = clock();
    printf("Tempo para listar os profissionais: %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
   

    start = clock();
    updateProf(prof, count, id2, "Kaua Bala", "Endocrionologista");
    end = clock();
    printf("Tempo para atualizar profissional: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");
    listProf(prof, count);

   
    start = clock();
    deleteProf(prof, &count, id3);
    end = clock();
    printf("Tempo para deletar profissional: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");
    listProf(prof, count);

  
    start = clock();
    deleteProf(prof, &count, id1);
    end = clock();
    printf("Tempo para deletar um profissional: %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);

    
    start = clock();
    deleteProf(prof, &count, id2);
    end = clock();
    printf("Tempo para deletar um profissional: %f segundos\n\n", (double)(end - start) / CLOCKS_PER_SEC);
    
   
    start = clock();
    salvaProfTxt(prof, count);
    end = clock();
    printf("Tempo para salvar profissionais para o arquivo txt: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");

    
    start = clock();
    carregaProfDoTxt(prof, &count);
    end = clock();
    printf("Tempo para carregar profissionais do arquivo txt: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");
    listProf(prof, count);

    
    start = clock();
    salvaProfNoBin(prof, count);
    end = clock();
    printf("Tempo para salvar profissionais para o arquivo binario: %f segundos\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");

    
    start = clock();
    carregaProfDoBin(prof, &count);
    end = clock();
    printf("Tempo para carregar profissionais do arquivo binario: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("\n");
    listProf(prof, count);

    return 0;
}