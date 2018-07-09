#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int max(int x,int y) {
	if(x > y)
		return x;
	else
		return y;
}
int LCS(char *X, char *Y, int m, int n) {

	int L[m+1][n+1];
	int i = 0;
	int j = 0;
	for(i = 0; i<=m;i++) {
		for(j = 0; j<=n; j++) {
			if(i == 0 || j == 0) {
				L[i][j] = 0;
			} else if(X[i-1] == Y[j - 1]) {
				L[i][j] = 1 + L[i-1][j-1];
			} else {
				L[i][j] = max(L[i-1][j],L[i][j-1]);
			}
		}
	}

	for(i = 0; i<=m;i++) {
		for(j = 0; j<=n; j++) {
			printf("%d ",L[i][j]);
		}
		printf("\n");
	}
//	printf("%d",L[m][n]);

}
int main(void) {

	char Y[] = "GXTXAB";
	char X[] = "AGGTAB";
	int n = strlen(Y);
	int m = strlen(X);
	LCS(Y,X,n,m);
	return 0;
}
