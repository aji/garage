use std::fmt;

use gl;
use gl::types::*;

pub enum Error {
    Gl(&'static str, u32, u32, GLenum),
    Other(&'static str),
}

pub type Result<T> = std::result::Result<T, Error>;

macro_rules! try_gl {
    ($x:expr) => {{
        let result = $x;
        match gl::GetError() {
            gl::NO_ERROR => result,
            e => return Err(crate::error::Error::Gl(file!(), line!(), column!(), e)),
        }
    }};
}

macro_rules! ww_assert {
    ($x:expr, $e:expr) => {{
        if !$x {
            return Err(Error::from($e));
        }
    }};
}

impl From<&'static str> for Error {
    fn from(e: &'static str) -> Error {
        Error::Other(e)
    }
}

impl fmt::Debug for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Gl(file, line, column, x) => {
                let msg = match *x {
                    gl::NO_ERROR => "GL_NO_ERROR".to_string(),
                    gl::INVALID_ENUM => "GL_INVALID_ENUM".to_string(),
                    gl::INVALID_VALUE => "GL_INVALID_VALUE".to_string(),
                    gl::INVALID_OPERATION => "GL_INVALID_OPERATION".to_string(),
                    gl::INVALID_FRAMEBUFFER_OPERATION => {
                        "GL_INVALID_FRAMEBUFFER_OPERATION".to_string()
                    }
                    gl::OUT_OF_MEMORY => "GL_OUT_OF_MEMORY".to_string(),
                    gl::STACK_UNDERFLOW => "GL_STACK_UNDERFLOW".to_string(),
                    gl::STACK_OVERFLOW => "GL_STACK_OVERFLOW".to_string(),
                    e => format!("GfxError::Gl({:?})", e),
                };
                write!(f, "{}:{}:{}: {}", file, line, column, msg)
            }
            Error::Other(x) => write!(f, "GfxError({})", x),
        }
    }
}
