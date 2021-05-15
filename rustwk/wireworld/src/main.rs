use glutin;
use glutin::event::{Event, WindowEvent};
use glutin::event_loop::{ControlFlow, EventLoop};
use glutin::window::WindowBuilder;
use glutin::ContextBuilder;

pub mod ca;

fn main() {
    let el = EventLoop::new();
    let wb = WindowBuilder::new().with_title("wireworld");

    let windowed_context = ContextBuilder::new().build_windowed(wb, &el).unwrap();
    let windowed_context = unsafe { windowed_context.make_current().unwrap() };

    println!(
        "Pixel format of the window's GL context: {:?}",
        windowed_context.get_pixel_format()
    );

    gl::load_with(|s| windowed_context.get_proc_address(s) as *const _);

    el.run(move |event, _, control_flow| {
        //println!("{:?}", event);
        *control_flow = ControlFlow::Wait;

        match event {
            Event::LoopDestroyed => return,
            Event::WindowEvent { event, .. } => match event {
                WindowEvent::Resized(size) => {
                    windowed_context.resize(size);
                }
                WindowEvent::CloseRequested => *control_flow = ControlFlow::Exit,
                _ => (),
            },
            _ => (),
        }

        windowed_context.swap_buffers().unwrap();
    });
}
