void setup() {
  size(1920, 1080);
}

void draw() {
  //drawTime(millis() / 1000.0);
  drawTime(frameCount / 60.0);
  saveFrame("out2/img######.png");
}

void drawTime(float t) {
  Complex z = Complex.of(0.5, t);
  Complex sum = Complex.zero();
  Complex sum2 = Complex.zero();
  Complex sum3 = Complex.zero();
  Complex sum4 = Complex.zero();
  background(200);
  for (int i=0; i<20000; i++) {
    Complex fz = term(z, i);
    Complex next = sum.add(fz);
    Complex next2 = sum2.add(next);
    Complex next3 = sum3.add(next2.mul(1. / (i + 2.)));
    Complex next4 = sum4.add(next3.mul(1. / (i + 2.)));
    stroke(0, 0, 0, 200);
    lineComplex(sum4.mul(1. / (i + 1.)), next4.mul(1. / (i + 2.)), 500);
    stroke(0, 0, 0, 150);
    lineComplex(sum3.mul(1. / (i + 1.)), next3.mul(1. / (i + 2.)), 500);
    stroke(0, 0, 0, 100);
    lineComplex(sum2.mul(1. / (i + 1.)), next2.mul(1. / (i + 2.)), 500);
    stroke(0, 0, 0, 50);
    lineComplex(sum, next, 500);
    sum = next;
    sum2 = next2;
    sum3 = next3;
    sum4 = next4;
  }
  text("t="+t, 10, 10);
}

Complex term(Complex s, int i) {
  return s.mul(-Math.log(i + 1)).exp();
}

void lineComplex(Complex z0, Complex z1, float scale) {
  PVector p0 = plot(z0, scale);
  PVector p1 = plot(z1, scale);
  line(p0.x, p0.y, p1.x, p1.y);
}

PVector plot(Complex z, float scale) {
  return new PVector(
    500         + map((float)z.re, 0, 1, 0,  scale),
    height / 2  + map((float)z.im, 0, 1, 0, -scale)
  );
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
