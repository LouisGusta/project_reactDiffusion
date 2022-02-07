int index(int x, int y) {
  return y*largura + x;
}

void desenha() {
  
  if(colorMode == 0) {
    pg.colorMode(RGB, 255, 255, 255);
    colorMode(RGB, 255, 255, 255);
  }
  else {
    pg.colorMode(HSB, 360, 100, 255);
    colorMode(HSB, 360, 100, 255);
  }
  
  for(int x = 0; x<largura; x++)
  for(int y = 0; y<altura; y++) {
    int i = index(x, y);
    float c = A[i] - B[i];
    c = constrain(c, 0, 1);
    if(colorMode == 0)
      pg.pixels[i] = color(map(c, 0, 1, red(cA), red(cB)), map(c, 0, 1, green(cA), green(cB)), map(c, 0, 1, blue(cA), blue(cB)));
    else if(colorMode == 1)
      pg.pixels[i] = color(degrees(atan2(y-altura/2,x-largura/2))+180, dist(x,y, largura/2, altura/2)*5, 255*(1-c));
    else
      pg.pixels[i] = color(map(dist(x,y, largura/2, altura/2), 0, maxDist, 0, 360), dist(x,y, largura/2, altura/2)*5, 255*(1-c));
  }
}

void atualiza() {
  
  for(int y = 0; y<altura; y++)
  for(int x = 0; x<largura; x++) {
    int i = index(x, y);
    
    nA[i] = A[i]
            + ( dA * laplace(A, x, y)
            - A[i] * B[i] * B[i]
            + f * (1 - A[i]) )
            * deltaT;
            
    nB[i] = B[i]
            + ( dB * laplace(B, x, y)
            + A[i] * B[i] * B[i]
            - (k + f) * B[i] )
            * deltaT;
            
  }
  
  float[] temp;
  
  temp = A;
  A = nA;
  nA = temp;
  
  temp = B;
  B = nB;
  nB = temp;
  
}

float laplace(float[] M, int x, int y) {
  float peso, soma = 0;
  for(int dx = -1; dx<=1; dx++)
  for(int dy = -1; dy<=1; dy++) {
    if(dx == 0 && dy == 0)
      peso = -1;
    else if(abs(dx) + abs(dy) == 2)
      peso = 0.05;
    else
      peso = 0.2;
      
    if(x + dx >=0 && x + dx < largura && y + dy >=0 && y + dy < altura)
      soma += peso * M[index(x+dx, y+dy)];
  }
  return soma;
}
