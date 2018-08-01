from rudaux import Course, Assignment


def initialize_course():

  course = Course()

  course                         \
    .get_external_tool_id()      \
    .get_students_from_canvas()  \
    .sync_nbgrader()             \
    .assign_all()                \
    .create_canvas_assignments()
