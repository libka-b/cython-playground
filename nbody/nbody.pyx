from libc.math cimport sqrt
from libc.stdlib cimport malloc, free

cdef struct body_t:
    double position[3]
    double velocity[3]
    double mass


cdef void make_cbodies(list bodies, body_t * cbodies, int num_bodies):
    cdef body_t * cbody
    for i, body in enumerate(bodies):
        if i >= num_bodies:
            break
        position, velocity, mass = body
        cbody = &cbodies[i]
        cbody.position[0], cbody.position[1], cbody.position[2] = position
        cbody.velocity[0], cbody.velocity[1], cbody.velocity[2] = velocity
        cbody.mass = mass


cdef list make_pybodies(body_t * bodies, int num_bodies):
    pybodies = []
    for i in range(num_bodies):
        pybodies.append(
            (
                [
                    bodies[i].position[0], bodies[i].position[1], bodies[i].position[2]
                ],
                [
                    bodies[i].velocity[0], bodies[i].velocity[1], bodies[i].velocity[2]
                ],
                bodies[i].mass
            )
        )


def advance(double delta, int steps, bodies):
    cdef:
        int num_bodies = len(bodies)
        int i, ii, jj
        double dx, dy, dz, mag, b1m, b2m
        body_t * body1
        body_t * body2
        body_t * cbodies = <body_t *>malloc(num_bodies * sizeof(body_t))

    if not cbodies:
        raise MemoryError("Not enough memory to allocate cbodies")

    make_cbodies(bodies, cbodies, num_bodies)

    for i in range(steps):
        for ii in range(num_bodies - 1):
            body1 = &cbodies[ii]
            for jj in range(ii + 1, num_bodies):
                body2 = &cbodies[jj]
                dx = body1.position[0] - body2.position[0]
                dy = body1.position[1] - body2.position[1]
                dz = body1.position[2] - body2.position[2]
                mag = delta / sqrt(dx * dx + dy * dy + dz * dz)
                b1m = body1.mass * mag
                b2m = body2.mass * mag
                body1.velocity[0] -= dx * b2m
                body1.velocity[1] -= dy * b2m
                body1.velocity[2] -= dz * b2m
                body2.velocity[0] -= dx * b1m
                body2.velocity[1] -= dy * b1m
                body2.velocity[2] -= dz * b1m
        for ii in range(num_bodies):
            body2 = &cbodies[ii]
            body2.position[0] += delta * body2.velocity[0]
            body2.position[1] += delta * body2.velocity[1]
            body2.position[2] += delta * body2.velocity[2]

    pybodies = make_pybodies(cbodies, num_bodies)
    free(cbodies)
    return pybodies
