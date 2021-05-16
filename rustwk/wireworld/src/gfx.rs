use gl;
use gl::types::*;

use crate::error::*;

const RENDER_VERT_GLSL: &'static [u8] = include_bytes!("vertex.glsl");
const RENDER_FRAG_GLSL: &'static [u8] = include_bytes!("fragment.glsl");

pub struct Renderer {
    prog: GLuint,

    u_viewport_size: GLint,
    u_grid_pos: GLint,
    u_grid_size: GLint,
    u_grid_zoom: GLint,

    a_pos: GLint,
}

impl Renderer {
    pub fn new() -> Result<Renderer> {
        unsafe {
            let prog = compile_render_program(RENDER_VERT_GLSL, RENDER_FRAG_GLSL)?;

            Ok(Renderer {
                prog,

                u_viewport_size: get_uniform_location(prog, b"u_viewport_size")?,
                u_grid_pos: get_uniform_location(prog, b"u_grid_pos")?,
                u_grid_size: get_uniform_location(prog, b"u_grid_size")?,
                u_grid_zoom: get_uniform_location(prog, b"u_grid_zoom")?,

                a_pos: get_attrib_location(prog, b"a_pos")?,
            })
        }
    }

    pub fn render(&self) {}
}

unsafe fn compile_render_program(vss: &'static [u8], fss: &'static [u8]) -> Result<GLuint> {
    let vs = try_gl!(gl::CreateShader(gl::VERTEX_SHADER));
    let fs = try_gl!(gl::CreateShader(gl::FRAGMENT_SHADER));

    try_gl!(gl::ShaderSource(
        vs,
        1,
        [vss.as_ptr() as *const _].as_ptr(),
        [vss.len() as GLint].as_ptr()
    ));
    try_gl!(gl::ShaderSource(
        fs,
        1,
        [fss.as_ptr() as *const _].as_ptr(),
        [fss.len() as GLint].as_ptr()
    ));

    try_gl!(gl::CompileShader(vs));
    try_gl!(gl::CompileShader(fs));

    let prog = try_gl!(gl::CreateProgram());
    try_gl!(gl::AttachShader(prog, vs));
    try_gl!(gl::AttachShader(prog, fs));
    try_gl!(gl::LinkProgram(prog));

    Ok(prog)
}

unsafe fn get_uniform_location(prog: GLuint, attr: &'static [u8]) -> Result<GLint> {
    Ok(try_gl!(gl::GetUniformLocation(
        prog,
        attr.as_ptr() as *const _
    )))
}

unsafe fn get_attrib_location(prog: GLuint, attr: &'static [u8]) -> Result<GLint> {
    Ok(try_gl!(gl::GetAttribLocation(
        prog,
        attr.as_ptr() as *const _
    )))
}
