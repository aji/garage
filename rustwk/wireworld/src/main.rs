use glutin;
use glutin::dpi::PhysicalSize;
use glutin::event::{Event, WindowEvent};
use glutin::event_loop::{ControlFlow, EventLoop};
use glutin::window::WindowBuilder;
use glutin::ContextBuilder;

#[macro_use]
pub mod error;

pub mod ca;
pub mod gfx;
pub mod math;

fn main() {
    let mut viewport_size = math::Vec2(1920, 1080);
    let grid_size = math::Vec2(300, 300);

    let el = EventLoop::new();
    let wb = WindowBuilder::new()
        .with_title("wireworld")
        .with_resizable(false)
        .with_inner_size(PhysicalSize::<u32>::from((
            viewport_size.0,
            viewport_size.1,
        )));

    let windowed_context = ContextBuilder::new().build_windowed(wb, &el).unwrap();
    let windowed_context = unsafe { windowed_context.make_current().unwrap() };

    gl::load_with(|s| windowed_context.get_proc_address(s) as *const _);
    let renderer = gfx::Renderer::new().expect("failed to create renderer");

    let inner_size = windowed_context.window().inner_size();
    viewport_size.0 = inner_size.width;
    viewport_size.1 = inner_size.height;

    let active = gfx::ActiveRenderer::open(renderer, viewport_size, grid_size)
        .expect("failed to open active renderer");

    el.run(move |event, _, control_flow| {
        //println!("{:?}", event);
        *control_flow = ControlFlow::Wait;

        match event {
            Event::LoopDestroyed => return,
            Event::WindowEvent { event, .. } => match event {
                WindowEvent::CloseRequested => *control_flow = ControlFlow::Exit,
                _ => (),
            },
            _ => (),
        }

        active
            .render(math::Vec2(20, 20), math::Vec2(1.0, 1.0))
            .unwrap();
        windowed_context.swap_buffers().unwrap();
    });
}
