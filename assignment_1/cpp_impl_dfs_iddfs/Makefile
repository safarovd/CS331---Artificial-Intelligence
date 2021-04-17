compile:
	clear
	g++ -std=c++11 driver.cpp stack.cpp -o prog 

dfs1:
	./prog ./starts/start1.txt ./goals/goal1.txt d output.txt

dfs2:
	./prog ./starts/start2.txt ./goals/goal2.txt d output.txt

dfs3:
	./prog ./starts/start3.txt ./goals/goal3.txt d output.txt

valdfs1:
	valgrind ./prog ./starts/start1.txt ./goals/goal1.txt d output.txt

valdfs2:
	valgrind ./prog ./starts/start2.txt ./goals/goal2.txt d output.txt
	
valdfs3:
	valgrind ./prog ./starts/start3.txt ./goals/goal3.txt d output.txt

iddfs1:
	./prog ./starts/start1.txt ./goals/goal1.txt i output.txt

iddfs2:
	./prog ./starts/start2.txt ./goals/goal2.txt i output.txt

iddfs3:
	./prog ./starts/start3.txt ./goals/goal3.txt i output.txt

validdfs1:
	valgrind ./prog ./starts/start1.txt ./goals/goal1.txt i output.txt

validdfs2:
	valgrind ./prog ./starts/start2.txt ./goals/goal2.txt i output.txt

validdfs3:
	valgrind ./prog ./starts/start3.txt ./goals/goal3.txt i output.txt