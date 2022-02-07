
float[] A, B, nA, nB;

PGraphics pg;

float dA, dB, f, k, deltaT;
int largura, altura, fps, totalFrames;
String enderecoVideo, enderecoThumb;
color cA, cB;
int cont = 0;

float escala;
float maxDist;
int colorMode;

JSONObject params, screen, drawing, metadata, colors;

void setup() {
  size(150,210,FX2D);
  
  params = loadJSONObject("params.json");
  screen = params.getJSONArray("screen").getJSONObject(0);
  
  largura     = screen.getInt("width");
  altura      = screen.getInt("height");
  fps         = screen.getInt("fps");
  totalFrames = screen.getInt("totalFrames");
  
  drawing = params.getJSONArray("drawing").getJSONObject(0);
  
  dA     = drawing.getFloat("dA");
  dB     = drawing.getFloat("dB");
  f      = drawing.getFloat("f");
  k      = drawing.getFloat("k");
  deltaT = drawing.getFloat("deltaT");
  
  metadata = params.getJSONArray("metadata").getJSONObject(0);
  
  enderecoVideo = metadata.getString("pathVideo");
  enderecoThumb = metadata.getString("pathThumb");
  
  colors = params.getJSONArray("colors").getJSONObject(0);
  
  colorMode = colors.getInt("mode");
  
  if(colorMode == 0) {
    int rA = colors.getInt("rA");
    int gA = colors.getInt("gA");
    int bA = colors.getInt("bA");
    cA = color(rA, gA, bA);
    
    int rB = colors.getInt("rB");
    int gB = colors.getInt("gB");
    int bB = colors.getInt("bB");
    cB = color(rB, gB, bB);
  }
  
  maxDist = dist(0,0, largura/2, altura/2);
  escala = min(150.0/largura, 150.0/altura);
  imageMode(CENTER);
  
  pg = createGraphics(largura, altura);
  
  // inicializa matrizes
  A  = new float[largura*altura];
  B  = new float[largura*altura];
  nA = new float[largura*altura];
  nB = new float[largura*altura];
  
  for(int i = 0; i<largura*altura; i++) {
    A[i] = 1;
    B[i] = 0;
    nA[i] = 1;
    nB[i] = 0;
  }
  
  for(int x = largura/2-10; x<largura/2+10; x++)
  for(int y = altura/2-10; y<altura/2+10; y++) {
    B[index(x,y)] = 1;
  }
  pg.beginDraw();
  pg.loadPixels();
}

void draw() {
  
  atualiza();
  atualiza();
  desenha();
  cont ++;
  
  background(0);
  
  pg.updatePixels();
  pg.endDraw();
  image(pg, 75, 135, largura*escala, altura*escala);
  
  if(cont%200 == 0 && !verifica()) {
    cont = totalFrames;
    pg.beginDraw();
    pg.stroke(0);
    pg.fill(0);
    pg.rect(0,0,largura,altura);
    pg.endDraw();
  }
  
  stroke(255);
  textSize(20);
  text(str(cont) + "/" + str(totalFrames) + "\n" + str(100*float(cont)/totalFrames) + "%", 10, 20);
  
  rec();
  
  if(cont==totalFrames) {
    videoExport.endMovie();
    pg.updatePixels();
    pg.endDraw();
    pg.save(enderecoThumb);
    exit(  );
  }
}

boolean verifica() {
  boolean diferente = false;
  for(int x = 50; x<largura-50 && !diferente; x++)
  for(int y = 50; y<altura-50 && !diferente; y++) {
    int i = index(x, y);
    float c = A[i] - B[i];
    c = constrain(c, 0, 1);
    if(c>0.1)
      diferente = true;
  }
  
  if(!diferente)
    return false;
  diferente = false;
    
  for(int x = 50; x<largura-50 && !diferente; x++)
  for(int y = 50; y<altura-50 && !diferente; y++) {
    int i = index(x, y);
    float c = A[i] - B[i];
    c = constrain(c, 0, 1);
    
    if(c<0.9)
      diferente = true;
  }
  if(!diferente)
    return false;
  return true;
}
