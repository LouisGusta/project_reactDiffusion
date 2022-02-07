final String sketchname = getClass().getName();

import com.hamoid.*;
VideoExport videoExport;

void rec() {
  if (frameCount == 1) {
    videoExport = new VideoExport(this, enderecoVideo, pg);
    videoExport.setFrameRate(fps);
    videoExport.setLoadPixels(false);
    videoExport.setDebugging(false);
    videoExport.startMovie();
  }
  videoExport.saveFrame();
}
