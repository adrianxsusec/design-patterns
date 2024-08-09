#include "myfactory.h"
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void* myfactory(char const* libname, char const* ctorarg) {
    void* handle;
    void* (*create)(char const*);
    char *error;
    handle = dlopen(libname, RTLD_LAZY);
    char fullname[256];

    strcpy(fullname, "./");
    strcat(fullname, libname);
    #ifdef _WIN32
        strcat(fullname, ".dll");
    #else
        strcat(fullname, ".so");
    #endif

    printf("Attempting to open library: %s\n", fullname);

    if (!handle) {
        fprintf(stderr, "Error opening library: %s\n", dlerror());
        return NULL;
    }

    printf("Library opened successfully. Attempting to find 'create' function.\n");
    
    create = (void* (*)(const char*)) dlsym(handle, "create");
    if ((error = dlerror()) != NULL)  {
        fprintf(stderr, "Error finding create function: %s\n", error);
        dlclose(handle);
        return NULL;
    }

    printf("'create' function found. Attempting to create object.\n");

    void* result = create(ctorarg);
    return result;
}