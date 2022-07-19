import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import com.hamoid.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class diffusionVideo extends PApplet {


float[] A, B, nA, nB;

PGraphics pg;

float dA, dB, f, k, deltaT;
int largura, altura, fps, apf, totalFrames;
String enderecoVideo, enderecoThumb;
int cA, cB;
int cont = 0;

float escala;
float maxDist;
int colorMode;

JSONObject params, screen, drawing, metadata, colors;

public void setup() {
  
  
  params = loadJSONObject("params.json");
  screen = params.getJSONArray("screen").getJSONObject(0);
  
  largura     = screen.getInt("width");
  altura      = screen.getInt("height");
  fps         = screen.getInt("fps");
  apf         = screen.getInt("apf");
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
  escala = min(150.0f/largura, 150.0f/altura);
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

public void draw() {
  
  for(int i = 0; i<apf; i++)
    atualiza();
  
  desenha();
  cont ++;
  
  background(0);
  
  pg.updatePixels();
  pg.endDraw();
  image(pg, 75, 135, largura*escala, altura*escala);
  
  if(cont%25 == 0 && !verifica()) {
    cont = totalFrames;
    pg.beginDraw();
    pg.stroke(0);
    pg.fill(0);
    pg.rect(0,0,largura,altura);
    pg.endDraw();
  }
  
  stroke(255);
  textSize(20);
  text(str(cont) + "/" + str(totalFrames) + "\n" + str(100*PApplet.parseFloat(cont)/totalFrames) + "%", 10, 20);
  
  rec();
  
  if(cont==totalFrames) {
    videoExport.endMovie();
    pg.updatePixels();
    pg.endDraw();
    pg.save(enderecoThumb);
    exit(  );
  }
}

public boolean verifica() {
  boolean diferente = false;
  for(int x = 50; x<largura-50 && !diferente; x++)
  for(int y = 50; y<altura-50 && !diferente; y++) {
    int i = index(x, y);
    float c = A[i] - B[i];
    c = constrain(c, 0, 1);
    if(c>0.1f)
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
    
    if(c<0.9f)
      diferente = true;
  }
  if(!diferente)
    return false;
  return true;
}
public int index(int x, int y) {
  return y*largura + x;
}

public void desenha() {
  
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

public void atualiza() {
  
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

public float laplace(float[] M, int x, int y) {
  float peso, soma = 0;
  for(int dx = -1; dx<=1; dx++)
  for(int dy = -1; dy<=1; dy++) {
    if(dx == 0 && dy == 0)
      peso = -1;
    else if(abs(dx) + abs(dy) == 2)
      peso = 0.05f;
    else
      peso = 0.2f;
      
    if(x + dx >=0 && x + dx < largura && y + dy >=0 && y + dy < altura)
      soma += peso * M[index(x+dx, y+dy)];
  }
  return soma;
}
final String sketchname = getClass().getName();


VideoExport videoExport;

public void rec() {
  if (frameCount == 1) {
    videoExport = new VideoExport(this, enderecoVideo, pg);
    videoExport.setFrameRate(fps);
    videoExport.setLoadPixels(false);
    videoExport.setDebugging(false);
    videoExport.startMovie();
  }
  videoExport.saveFrame();
}
  public void settings() {  size(150,210,FX2D); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "diffusionVideo" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
