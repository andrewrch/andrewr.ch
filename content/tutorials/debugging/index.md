% Debugging C and C++
% Andrew Chambers
% 27/2/2014

This is a short tutorial intended to give some basic advice on how to debug C
and C++ code.

Compiling
---------

If using gcc or g++, compile code using the -g flag.  This compiles while adding debugging symbols to 
the binary.  This is important so that your debugger is able to trace variable 
names as well as line numbers in your source.

    $ gcc -g <source_files> -o <binary_name>

If you have finished debugging your code, either remove the -g from your 
makefile and rebuild, or you can use the strip utility

Using valgrind
--------------

Depending on what I am debugging, I might just run my program through valgrind.  

    $ valgrind <program_name> <program_args>

This is a virtual environment which tracks mallocs and frees which is useful for 
finding memory leaks, but also gives infomation when a program has attempted a 
memory read or write somewhere it shouldn't have


~~~~ {#mycode data-language=c}
    #include <stdio.h>
    #include <stdlib.h>

    int main() {
      int* array = (int*) malloc(2 * sizeof(int));

      printf("After end of array: %d\n", array[2]);
      return EXIT_SUCCESS;
    }
~~~~

The above code allocates a pointer to space for 2 ints, but then prints the 
value of the int at element index 2, which hasn't been allocated.  According to 
the C specification, this gives undefined behaviour, which is bad!  If we run

    $ valgrind ./valgrind_example

Then we get this output

    ==7387== Memcheck, a memory error detector
    ==7387== Copyright (C) 2002-2012, and GNU GPL'd, by Julian Seward et al.
    ==7387== Using Valgrind-3.8.1 and LibVEX; rerun with -h for copyright info
    ==7387== Command: ./valgrind_example
    ==7387== 
    ==7387== Invalid read of size 4
    ==7387==    at 0x40059B: main (valgrind_example.c:7)
    ==7387==  Address 0x51fc048 is 0 bytes after a block of size 8 alloc'd
    ==7387==    at 0x4C2A2DB: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==7387==    by 0x40058E: main (valgrind_example.c:5)
    ==7387== 
    After end of array: 0
    ==7387== 
    ==7387== HEAP SUMMARY:
    ==7387==     in use at exit: 8 bytes in 1 blocks
    ==7387==   total heap usage: 1 allocs, 0 frees, 8 bytes allocated
    ==7387== 
    ==7387== LEAK SUMMARY:
    ==7387==    definitely lost: 8 bytes in 1 blocks
    ==7387==    indirectly lost: 0 bytes in 0 blocks
    ==7387==      possibly lost: 0 bytes in 0 blocks
    ==7387==    still reachable: 0 bytes in 0 blocks
    ==7387==         suppressed: 0 bytes in 0 blocks
    ==7387== Rerun with --leak-check=full to see details of leaked memory
    ==7387== 
    ==7387== For counts of detected and suppressed errors, rerun with: -v
    ==7387== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 2 from 2)

Let's look at the output.  At the beginning of every line is printed <code>==7387==</code>.  This is the process ID and is not
important.  The first few lines give information about the version of valgrind 
we've used and the command we have run, but the more important information 
follows, and we can break it down line by line, note I've cut out a few bits 
which aren't important here.

    Invalid read of size 4

This tells us we have attempted to read 4 bytes somewhere in memory we shouldn't have.

    main (valgrind_example.c:7)

This tells us the function the read occured in (<code>main</code>), the source 
file that contains the function (<code>valgrind_example.c</code>) and even on 
which line of the source file the offending read occurs (<code>:7</code>).

    Address 0x51fc048 is 0 bytes after a block of size 8 alloc'd

This line tells us that the read comes immediately (0 bytes) after some memory 
we have allocated.  The allocation was for 8 bytes or memory, or in other words 
the size of 2 ints on this machine.

    at 0x4C2A2DB: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
    by 0x40058E: main (valgrind_example.c:5)

Finally we are told where malloc was called to allocate those 8 bytes of memory: 
In <code>valgrind_example.c</code> on line 5.

At the bottom of the output, we are given information about the 
