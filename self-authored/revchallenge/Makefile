CC      ?= gcc
CFLAGS  ?= -O2 -Wall

all: scorequest

scorequest: challenge.c flag_data.h
	$(CC) $(CFLAGS) -o scorequest challenge.c

# Regenerate the encrypted flag header (optionally set FLAG="...")
flag_data.h: gen_flag.py
	python3 gen_flag.py

clean:
	rm -f scorequest flag_data.h

.PHONY: all clean
