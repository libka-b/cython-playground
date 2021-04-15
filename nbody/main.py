import sys
from typing import Dict, List, Tuple

from common import timeit

from nbody import advance


Body = Tuple[List[float], List[float], float]


def combinations(bodies: List[Body]) -> List[Tuple[Body, Body]]:
    result = []
    for x in range(len(bodies) - 1):
        ls = bodies[x + 1:]
        for y in ls:
            result.append((bodies[x], y))
    return result


def advance_py(delta: float, steps: int, bodies: List[Body], pairs: List[Tuple[Body, Body]]) -> None:
    for i in range(steps):
        for (([x1, y1, z1], v1, m1),
                ([x2, y2, z2], v2, m2)) in pairs:
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            mag = delta * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            b1m = m1 * mag
            b2m = m2 * mag
            v1[0] -= dx * b2m
            v1[1] -= dy * b2m
            v1[2] -= dz * b2m
            v2[0] += dx * b1m
            v2[1] += dy * b1m
            v2[2] += dz * b1m
        for (r, [vx, vy, vz], m) in bodies:
            r[0] += delta * vx
            r[1] += delta * vy
            r[2] += delta * vz


def report_energy(bodies: List[Body], pairs: List[Tuple[Body, Body]]) -> None:
    e = 0.0
    for (((x1, y1, z1), _, m1),
            ((x2, y2, z2), _, m2)) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    for (_, [vx, vy, vz], m) in bodies:
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
    print("%.9f" % e)


def offset_momentum(ref: Body, bodies: List[Body]) -> None:
    px = py = pz = 0.0
    for (_, [vx, vy, vz], m) in bodies:
        px -= vx * m
        py -= vy * m
        pz -= vz * m
    (_, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES: Dict[str, Body] = {
    "sun": (
        [
            0.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            0.0
        ],
        SOLAR_MASS
    ),
    "jupiter": (
        [
            4.84143144246472090e+00,
            -1.16032004402742839e+00,
            -1.03622044471123109e-01
        ],
        [
            1.66007664274403694e-03 * DAYS_PER_YEAR,
            7.69901118419740425e-03 * DAYS_PER_YEAR,
            -6.90460016972063023e-05 * DAYS_PER_YEAR
        ],
        9.54791938424326609e-04 * SOLAR_MASS
    ),
    "saturn": (
        [
            8.34336671824457987e+00,
            4.12479856412430479e+00,
            -4.03523417114321381e-01
        ],
        [
            -2.76742510726862411e-03 * DAYS_PER_YEAR,
            4.99852801234917238e-03 * DAYS_PER_YEAR,
            2.30417297573763929e-05 * DAYS_PER_YEAR
        ],
        2.85885980666130812e-04 * SOLAR_MASS
    ),
    "uranus": (
        [
            1.28943695621391310e+01,
            -1.51111514016986312e+01,
            -2.23307578892655734e-01
        ],
        [
            2.96460137564761618e-03 * DAYS_PER_YEAR,
            2.37847173959480950e-03 * DAYS_PER_YEAR,
            -2.96589568540237556e-05 * DAYS_PER_YEAR
        ],
        4.36624404335156298e-05 * SOLAR_MASS
    ),
    "neptune": (
        [
            1.53796971148509165e+01,
            -2.59193146099879641e+01,
            1.79258772950371181e-01
        ],
        [
            2.68067772490389322e-03 * DAYS_PER_YEAR,
            1.62824170038242295e-03 * DAYS_PER_YEAR,
            -9.51592254519715870e-05 * DAYS_PER_YEAR
        ],
        5.15138902046611451e-05 * SOLAR_MASS
    )
}


@timeit
def main_py(steps: int, bodies: Dict[str, Body], ref: str = "sun") -> None:
    system: List[Body] = list(bodies.values())
    pairs: List[Tuple[Body, Body]] = combinations(system)
    offset_momentum(bodies[ref], system)
    report_energy(system, pairs)
    advance_py(0.01, steps, system, pairs)
    report_energy(system, pairs)


@timeit
def main(steps: int, bodies: Dict[str, Body], ref: str = "sun") -> None:
    system = list(bodies.values())
    offset_momentum(bodies[ref], system)
    pairs = combinations(system)
    report_energy(system, pairs)
    advance(0.01, steps, system)


if __name__ == "__main__":
    main_py(int(sys.argv[1]), bodies=dict(**BODIES), ref="sun")
    main(int(sys.argv[1]), bodies=dict(**BODIES), ref="sun")

