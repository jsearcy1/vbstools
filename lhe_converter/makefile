# ROOT Lib
RootLibs= `root-config --libs`
RootHeader = `root-config --cflags`

# Compiler Setting
Inlude = -I. 
Debug = -g -O3 -Wall
Compile = g++ ${Debug} $(Include) $(RootHeader) 

# Code
AllSource=$(SideSource) $(RootDict) $(MainSource)
SideSource=
MainSource=convert.C
RootClass=
RootDict=

EXE=run-convert.exe

all : $(AllSource)
	@echo "<Now start to compile>"
	$(Compile) $(AllSource) $(RootLibs) -lTreePlayer -o $(EXE)
	@echo "<Done>"

clean:
	\rm -f *.o *.so *.exe
