use std::convert::TryInto;
use std::ffi::CStr;

use gl;
use gl::types::*;

use crate::error::Result;
use crate::math::Vec2;

const RENDER_VERT_GLSL: &'static [u8] = include_bytes!("vertex.glsl");
const RENDER_FRAG_GLSL: &'static [u8] = include_bytes!("fragment.glsl");

#[repr(C)]
pub struct GridAttrsSSBO {
    rows: i32,
    cols: i32,
    stride: i32,
    offset: i32,
    page: i32,
    page_size: i32,
}

#[derive(Debug)]
pub struct Renderer {
    prog: GLuint,

    ww_grid_attrs_block: GLuint,
    ww_grid_data_block: GLuint,

    u_viewport_size: GLint,
    u_grid_size: GLint,
    u_grid_pos: GLint,
    u_grid_zoom: GLint,

    a_pos: GLint,
}

impl Renderer {
    pub fn new() -> Result<Renderer> {
        unsafe {
            println!(
                "GL version: {}",
                CStr::from_ptr(gl::GetString(gl::VERSION) as *const _)
                    .to_str()
                    .unwrap()
            );
            let prog = compile_render_program(RENDER_VERT_GLSL, RENDER_FRAG_GLSL)?;

            Ok(Renderer {
                prog,

                ww_grid_attrs_block: 1,
                ww_grid_data_block: 2,

                u_viewport_size: get_uniform_location(prog, b"u_viewport_size\0")?,
                u_grid_size: get_uniform_location(prog, b"u_grid_size\0")?,
                u_grid_pos: get_uniform_location(prog, b"u_grid_pos\0")?,
                u_grid_zoom: get_uniform_location(prog, b"u_grid_zoom\0")?,

                a_pos: get_attrib_location(prog, b"a_pos\0")?,
            })
        }
    }

    pub fn close(self) {}
}

pub struct ActiveRenderer {
    render: Renderer,
    ww_grid_buf: GLuint,
    a_pos_buf: GLuint,
}

const CORNERS: &'static [f32] = &[-1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0];

impl ActiveRenderer {
    pub fn open(
        render: Renderer,
        viewport_size: Vec2<u32>,
        grid_size: Vec2<u32>,
    ) -> Result<ActiveRenderer> {
        unsafe {
            gl::Viewport(0, 0, viewport_size.0 as i32, viewport_size.1 as i32);
            gl::FrontFace(gl::CCW);

            gl::UseProgram(render.prog);

            uniform2f(render.u_viewport_size, viewport_size)?;
            uniform2f(render.u_grid_size, grid_size)?;

            let mut ww_grid_buf: GLuint = 0;
            try_gl!(gl::GenBuffers(1, &mut ww_grid_buf));
            try_gl!(gl::BindBuffer(gl::SHADER_STORAGE_BUFFER, ww_grid_buf));
            try_gl!(gl::BindBufferBase(
                gl::SHADER_STORAGE_BUFFER,
                render.ww_grid_block,
                ww_grid_buf
            ));

            let a_pos = render.a_pos.try_into().expect("a_pos has unexpected value");
            let mut a_pos_buf: GLuint = 0;
            try_gl!(gl::GenBuffers(1, &mut a_pos_buf));
            try_gl!(gl::BindBuffer(gl::ARRAY_BUFFER, a_pos_buf));
            try_gl!(gl::BufferData(
                gl::ARRAY_BUFFER,
                std::mem::size_of_val(CORNERS) as GLsizeiptr,
                CORNERS.as_ptr() as *const _,
                gl::STATIC_DRAW,
            ));
            try_gl!(gl::VertexAttribPointer(
                a_pos,
                2,
                gl::FLOAT,
                0,
                0,
                0 as *const _,
            ));
            try_gl!(gl::EnableVertexAttribArray(a_pos));

            Ok(ActiveRenderer {
                render,
                ww_grid_buf,
                a_pos_buf,
            })
        }
    }

    pub fn close(self) -> Renderer {
        unsafe {
            gl::DeleteBuffers(1, &self.ww_grid_buf);
            gl::DeleteBuffers(1, &self.a_pos_buf);
            self.render
        }
    }

    pub fn set_ww_grid<'a>(&self, grid: &'a GridSSBO) -> Result<()> {
        unsafe {
            gl::BindBuffer(gl::SHADER_STORAGE_BUFFER, self.ww_grid_buf);

            Ok(())
        }
    }

    pub fn render(&self, grid_pos: Vec2<i32>, grid_zoom: Vec2<f32>) -> Result<()> {
        unsafe {
            uniform2f(self.render.u_grid_pos, grid_pos)?;
            uniform2f(self.render.u_grid_zoom, grid_zoom)?;
            gl::DrawArrays(gl::TRIANGLE_FAN, 0, 4);
            Ok(())
        }
    }
}

unsafe fn uniform2f<T>(loc: GLint, v: Vec2<T>) -> Result<()>
where
    f64: From<T>,
{
    Ok(try_gl!(gl::Uniform2f(
        loc,
        f64::from(v.0) as GLfloat,
        f64::from(v.1) as GLfloat
    )))
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
