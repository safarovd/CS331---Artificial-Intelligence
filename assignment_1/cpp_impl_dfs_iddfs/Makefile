compile:
	clear
	g++ -std=c++11 driver.cpp stack.cpp -o prog 

dfs1:
	./prog ./starts/start1.txt ./goals/goal1.txt dfs output.txt

dfs2:
	./prog ./starts/start2.txt ./goals/goal2.txt dfs output.txt

dfs3:
	./prog ./starts/start3.txt ./goals/goal3.txt dfs output.txt

valdfs1:
	valgrind --leak-check=full ./prog ./starts/start1.txt ./goals/goal1.txt dfs output.txt

valdfs2:
	valgrind --leak-check=full ./prog ./starts/start2.txt ./goals/goal2.txt dfs output.txt
	
valdfs3:
	valgrind --leak-check=full ./prog ./starts/start3.txt ./goals/goal3.txt dfs output.txt

iddfs1:
	./prog ./starts/start1.txt ./goals/goal1.txt iddfs output.txt

iddfs2:
	./prog ./starts/start2.txt ./goals/goal2.txt iddfs output.txt

iddfs3:
	./prog ./starts/start3.txt ./goals/goal3.txt iddfs output.txt

validdfs1:
	valgrind --leak-check=full ./prog ./starts/start1.txt ./goals/goal1.txt iddfs output.txt

validdfs2:
	valgrind --leak-check=full ./prog ./starts/start2.txt ./goals/goal2.txt iddfs output.txt

validdfs3:
	valgrind --leak-check=full ./prog ./starts/start3.txt ./goals/goal3.txt iddfs output.txt