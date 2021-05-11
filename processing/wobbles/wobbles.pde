void setup() {
  size(1000, 200);
}

void draw() {
  background(0);
  stroke(255);
  for (int x=0; x<width; x+=2) {
    float y = map(
      wave(map(x, 0, width, 0.0, 1.0)),
      -1.0, 1.0, height-10, 10);
    line(x, y, x, height/2);
  }
  if (frameCount == 1) {
    saveFrame("frame.png");
  }
}

float wave(float x) {
  return
    0.3 * sin(x *  50 + millis() / 1900.0) +
    0.2 * sin(x *  60 - millis() / 1100.0) +
    0.2 * sin(x * 130 + millis() / 1100.0) +
    0.1 * sin(x * 570 + millis() /  500.0);
}
