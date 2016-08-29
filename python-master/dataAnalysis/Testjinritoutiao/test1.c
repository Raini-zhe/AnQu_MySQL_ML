#include <stdio.h>

int main(){
	int a,b;
	while(scanf("%d %d",&a,&b) != EOF){
		int count = 0;
		for(int i = 1;;i ++){
			if(a + i == a|i)
				count++;
			if(count == b)
				return i;
		}
	}
	return 0;
}