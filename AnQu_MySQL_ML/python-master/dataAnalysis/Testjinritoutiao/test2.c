#include <stdio.h>

void judge(int len[],int &num,int op,int lenc){
	if(op == 1){
		num ++;
		len[num-1] = lenc;
	}
	else{
		for(int j = 0; j < num;j++){
			if(len[j] == lenc)
			{
				while(j < num){
					len[j] = len[j+1];
					j++;
				}
				num --;
				break;
			}
		}
	}
	if(num < 3){
		printf("No\n");
	}
	else if(num >= 3){
		int max = len[0];
		int sum = 0;
		for(int j = 1;j < num;j--){
			if(max > len[j]){
				sum += max;
				max = len[j];
			}
			else{
				sum = len[j];
			}
		}
		if(max < sum){
			printf("yes");
		}
	}
}


int main(){
	int n;
	while(scanf("%d",&n) != EOF){
		int len[n];
		int op,lenc;
		int num = 0;
		int i = 0;
		while(scanf("%d %d",&op,&lenc) != EOF&&i < n)
		{
			judge(len,num,op,lenc);
			i++;
		}
	}
	return 0;
}