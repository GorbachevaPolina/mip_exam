import numpy as np
import matplotlib.pyplot as plt


class PolynomialViaPoint:
    def __init__(self, data):
        self.data = data
        self.coef = dict()

    def get_coef(self):
        for i in range(len(data) - 1):
            T = data[i]['time']
            delta_T = data[i+1]['time'] - T
            b_i = data[i]['b']
            db_i = data[i]['db']
            b_i1 = data[i+1]['b']
            db_i1 = data[i+1]['db']

            a0 = data[i]['b']
            a1 = data[i]['db']
            a2 = (3 * b_i1 - 3 * b_i - 2 * db_i * delta_T - db_i1 * delta_T) / delta_T ** 2
            a3 = (2 * b_i + (db_i + db_i1) * delta_T - 2 * b_i1) / delta_T ** 3

            self.coef[T] = [a0, a1, a2, a3]

    def get_trajectory(self, t):
        for delta_T, coef in reversed(self.coef.items()):
            if t >= delta_T:
                delta_t = t - delta_T
                return coef[0] + coef[1] * delta_t + coef[2] * delta_t ** 2 + coef[3] * delta_t ** 3

    def plot_results(self):
        self.get_coef()

        step = 0.01
        times = [t['time'] for t in data]

        t = np.arange(min(times), max(times) + step, step)
        pos = np.array(list(map(self.get_trajectory, t)))
        v = []
        for i in range(len(t) - 1):
            v.append([(pos[i + 1][0] - pos[i][0]) / step, (pos[i + 1][1] - pos[i][1]) / step])

        coords = plt.subplot2grid((2, 2), (0, 0))
        velocity = plt.subplot2grid((2, 2), (1, 0))
        trajectory = plt.subplot2grid((2, 2), (0, 1), rowspan=2)

        coords.plot(t, pos)
        coords.legend(['x', 'y'])
        coords.set_title('coordinates')
        coords.grid()

        velocity.plot(t[:-1], v)
        velocity.legend(['dx', 'dy'])
        velocity.set_title('velocity')
        velocity.grid()

        trajectory.plot(pos[:, 0], pos[:, 1])
        trajectory.set_title('trajectory')
        trajectory.grid()

        points_x = [point['b'][0] for point in data]
        points_y = [point['b'][1] for point in data]

        trajectory.scatter(points_x, points_y)
        for i in range(len(points_x)):
            text = f"({points_x[i]},{points_y[i]})"
            trajectory.annotate(text, (points_x[i], points_y[i]))

        plt.tight_layout()
        plt.show()


data = [
    {
        'time': 0,
        'b': np.array([0, 0]),
        'db': np.array([0, 0])
    },
    {
        'time': 1,
        'b': np.array([0, 1]),
        'db': np.array([1, 0])
    },
    {
        'time': 2,
        'b': np.array([1, 1]),
        'db': np.array([0, -1])
    },
    {
        'time': 3,
        'b': np.array([1, 0]),
        'db': np.array([0, 0])
    }
]
interpolation = PolynomialViaPoint(data)
interpolation.plot_results()