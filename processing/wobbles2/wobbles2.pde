color c_bg = #232323;
color c_ax = #505050;
color c_fg = #a0c000;

float angleX = 0;
float angleY = 0;
float angleWantX = 0;
float angleWantY = 0;

void setup() {
  size(1920, 1080);
}

void draw() {
  angleX = lerp(angleX, angleWantX, 0.1);
  //angleY = lerp(angleY, angleWantY, 0.1);
  if (mousePressed) {
    angleWantX = map(mouseX, 0, width, -PI, PI);
    angleWantY = map(mouseY, 0, height, -PI, PI);
  }
  drawActual(millis() / 1000.0);
  //angleWantX = (float)(PI * Math.floor(frameCount / 400.0) / 4.0) + 0.2;
  //angleWantY = 0.5 + 0.3 * (float)Math.sin(frameCount / 100.0);
  //angleWantX = frameCount / 400.0;
  //angleWantY = 0.3;
  drawActual(frameCount / 60.0);
  //saveFrame("out/wobbles#######.png");
}

void drawActual(double t) {
  background(c_bg);
  stroke(c_ax);
  strokeWeight(1);
  for (int i=0; i<=300; i++) {
    float xx = map(i, 0, 300, -1.0, 1.0);
    Complex z = wave(xx, t);
    PVector zero = plot(xx, Complex.zero(), (float)t);
    PVector p = plot(xx, z, (float)t);
    line(zero.x, zero.y, p.x, p.y);
  }
  stroke(c_ax);
  strokeWeight(5);
  PVector ax0 = plot(-1.0, Complex.zero(), (float)t);
  PVector ax1 = plot( 1.0, Complex.zero(), (float)t);
  line(ax0.x, ax0.y, ax1.x, ax1.y);
  stroke(c_fg);
  strokeWeight(5);
  strokeJoin(ROUND);
  noFill();
  beginShape();
  for (int i=0; i<=1000; i++) {
    float xx = map(i, 0, 1000, -1.0, 1.0);
    Complex z = wave(xx, t);
    PVector p = plot(xx, z, (float)t);
    vertex(p.x, p.y);
  }
  endShape();
}

PVector plot(float x, Complex z, float t) {
  PVector pxz = new PVector(x * 10, (float)z.re);
  pxz.rotate(angleX);
  PVector pzy = new PVector(pxz.y, (float)z.im);
  pzy.rotate(angleY);
  /*
  return new PVector(
    width / 2   + map(pxz.x / (20 + pzy.x),  0.0, 1.0, 0.0,  1000),
    height / 2  + map(pzy.y / (20 + pzy.x),  0.0, 1.0, 0.0, -1000)
  );
  */
  return new PVector(
    width / 2   + map(pxz.x,  0.0, 1.0, 0.0,  80),
    height / 2  + map(pzy.y,  0.0, 1.0, 0.0, -80)
  );
}

float rotation(float t) {
  t = t % 1.0;
  if (t < 0.3) {
    return 0;
  } if (t < 0.5) {
    return map(sin(map(t, 0.3, 0.5, -HALF_PI, HALF_PI)), -1.0, 1.0, 0.0, 1.0);
  } if (t < 0.8) {
    return 1.0;
  } else {
    return map(sin(map(t, 0.8, 1.0, HALF_PI, -HALF_PI)), -1.0, 1.0, 0.0, 1.0);
  }
}

Complex wave(double x, double t) {
  return Complex.zero()
    .add(Complex.of(0,   4 * x - t / 0.70).exp().mul(1.5))
    .add(Complex.of(0, -11 * x - t / 1.96).exp().mul(1.6))
    .add(Complex.of(0,  10 * x + t / 1.00).exp().mul(0.5))
    .add(Complex.of(0, -50 * x - t / 1.20).exp().mul(0.3))
    .add(Complex.of(0, -80 * x - t / 0.30).exp().mul(0.3))
    ;
}

static class Complex {
  double re, im;
  Complex(double re, double im) { this.re = re; this.im = im; }
  static Complex of(double re, double im) { return new Complex(re, im); }
  static Complex zero() { return new Complex(0, 0); }
  double arg() { return Math.atan2(im, re); }
  double abs() { return Math.sqrt(re * re + im * im); }
  Complex add(Complex z) { return new Complex(re + z.re, im + z.im); }
  Complex mul(Complex z) { return new Complex(re * z.re - im * z.im, re * z.im + im * z.re); }
  Complex mul(double s) { return new Complex(re * s, im * s); }
  Complex exp() { double r = Math.exp(re); return new Complex(r * Math.cos(im), r * Math.sin(im)); }
}
