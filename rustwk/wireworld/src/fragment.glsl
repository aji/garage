uniform vec2 u_viewport_size;
uniform vec2 u_grid_size;
uniform vec2 u_grid_pos;
uniform vec2 u_grid_zoom;

void main() {
    vec2 pos = vec2(gl_FragCoord.x, u_viewport_size.y - gl_FragCoord.y);

    vec2 rect_tl = u_grid_pos.xy;
    vec2 rect_br = u_grid_pos.xy + u_grid_size.xy * u_grid_zoom.xy;

    if (rect_tl.x <= pos.x && pos.x <= rect_br.x &&
        rect_tl.y <= pos.y && pos.y <= rect_br.y) {
        gl_FragColor = vec4(0.0, 0.4, 0.8, 1.0);
    } else {
        gl_FragColor = vec4(0.0, 0.1, 0.4, 1.0);
    }
}