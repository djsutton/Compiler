all: objects

objects: hashtable_itr.o  hashtable.o  hashtable_utility.o  runtime.o

%.o: %.c
	gcc -m32 -Wall -O3 -c $<
	
%: %.py hashtable_itr.o  hashtable.o  hashtable_utility.o  runtime.o compile.py
	compile.py $<
	gcc -Wall -m32 -O3 -o $@ *.o $@.s -lm
