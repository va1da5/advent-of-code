#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vector_s {
  int capacity;
  int index;
  int *array;
  void (*append)(struct Vector_s *self, int item);
  void (*expand)(struct Vector_s *self);
  void (*sort)(struct Vector_s *self);
  int (*count_sorted)(struct Vector_s *self, int needle);
} Vector_t;

int compare(const void *a, const void *b) { return (*(int *)a - *(int *)b); }

void sort(Vector_t *self) {
  qsort(self->array, self->index, sizeof(self->array[0]), compare);
}

int count_sorted(Vector_t *self, int needle) {
  int count = 0;

  for (int i = 0; i < self->index; i++) {
    int value = self->array[i];
    if (value > needle) {
      return count;
    }

    if (value == needle)
      count++;
  }

  return count;
}

void expand(Vector_t *self) {
  int newSize = self->capacity * 2;
  int *newArray = (int *)malloc(newSize * sizeof(int));

  if (!newArray) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // initiate with known values
  memset(newArray, 0, newSize);

  // copy old array into the new one
  memcpy(newArray, self->array, self->capacity * sizeof(int));

  // release old array
  free(self->array);

  self->array = newArray;
  self->capacity = newSize;
}

void append(Vector_t *self, int item) {
  if (self->index >= self->capacity) {
    self->expand(self);
  }

  self->array[self->index++] = item;
  return;
}

Vector_t makeVector(int initialCapacity) {
  Vector_t vector;
  vector.capacity = initialCapacity;
  vector.index = 0;
  vector.array = (int *)malloc(vector.capacity * sizeof(int));

  if (!vector.array) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }

  // flush memory
  memset(vector.array, 0, vector.capacity * sizeof(int));

  vector.expand = expand;
  vector.append = append;
  vector.sort = sort;
  vector.count_sorted = count_sorted;

  return vector;
}

void print(Vector_t *vector) {
  printf("[ ");
  for (int i = 0; i < vector->index; i++) {
    printf("%d, ", vector->array[i]);
  }
  printf("]\n");
}

int main(void) {

  FILE *file_p;

  Vector_t numbers[2] = {makeVector(10), makeVector(10)};

  char ch;
  char buffer[8];

  file_p = fopen("/workspaces/advent-of-code-in-c-2024/src/input.txt", "r");

  if (file_p == NULL) {
    printf("File cannot be opened");
    return EXIT_FAILURE;
  }

  char bufferIndex = 0;
  char numberSide = 0;

  while (1) {
    ch = fgetc(file_p);

    if (ch == ' ' || ch == '\n' || ch == EOF) {
      if (bufferIndex == 0)
        continue;

      int value = atoi(buffer);

      bufferIndex = 0;
      memset(buffer, 0, sizeof(buffer));

      numbers[numberSide].append(&numbers[numberSide], value);

      if (numberSide > 0)
        numberSide = -1;
      numberSide++;

      if (ch == EOF) {
        break;
      }

      continue;
    }

    buffer[bufferIndex] = ch;
    bufferIndex++;
  }

  fclose(file_p);

  for (int i = 0; i < 2; i++) {
    numbers[i].sort(&numbers[i]);
  }

  int out = 0;

  for (int i = 0; i < numbers[0].index; i++) {
    out += abs(numbers[0].array[i] - numbers[1].array[i]);
  }

  printf("Part 1: %d\n\n", out);

  out = 0;
  for (int i = 0; i < numbers[0].index; i++) {
    int left_value = numbers[0].array[i];
    out += left_value * numbers[1].count_sorted(&numbers[1], left_value);
  }

  printf("Part 2: %d\n\n", out);

  return 0;
}