int t;

void setup() {
  t=0;
  size(1920, 1080);
}

void draw() {
  t+=1;
  if (mousePressed) {
    fill(0);
  } else {
    fill(255);
  }
  ellipse(mouseX, mouseY, 80, 80);
  saveFrame("dots-######.png");
}
