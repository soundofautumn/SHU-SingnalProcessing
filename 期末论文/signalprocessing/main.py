from __future__ import annotations

from matplotlib import animation
from matplotlib import pyplot as plt

from Wave import *


class UpdateDist:
    """
    UpdateDist is a class that can update the figure
    """

    def __init__(self, figure, x, *func_y):
        self.figure = figure
        self.func_message, self.func_carrier, self.func_modulated = func_y
        self.xlim = 4
        self.ylim = 4

        self.ax1 = self.figure.add_subplot(3, 1, 1)  # message
        self.ax1.set_xlim(0, self.xlim)
        self.ax1.set_ylim(-self.ylim, self.ylim)
        self.ax1.set_title('message')
        self.ax1.set_xticks([])

        self.ax2 = self.figure.add_subplot(3, 1, 2)  # carrier
        self.ax2.set_xlim(0, self.xlim)
        self.ax2.set_ylim(-self.ylim, self.ylim)
        self.ax2.set_title('carrier')
        self.ax2.set_xticks([])

        self.ax3 = self.figure.add_subplot(3, 1, 3)  # modulate
        self.ax3.set_xlim(0, self.xlim)
        self.ax3.set_ylim(-self.ylim, self.ylim)
        self.ax3.set_title('modulate')
        self.ax3.set_xticks([])

        self.t = np.arange(0, 2 * np.pi, 0.01)  # time scale

        self.time = x
        self.line_message, = self.ax1.plot(self.time, self.func_message(self.time), 'k-')
        self.line_carrier, = self.ax2.plot(self.time, self.func_carrier(self.time), 'k-')
        self.line_modulated, = self.ax3.plot(self.time, self.func_modulated(self.time), 'k-')

    def __call__(self, i):
        self.line_message.set_data(self.time, self.func_message(self.time + i / 10))
        self.line_carrier.set_data(self.time, self.func_carrier(self.time + i / 10))
        self.line_modulated.set_data(self.time, self.func_modulated(self.time + i / 10))
        return self.line_message, self.line_carrier, self.line_modulated


def am_modulate(carrier_wave: TrigonometricWave, modulate_wave: Wave, k_a=1) -> Wave:
    return (k_a / carrier_wave.amplitude * modulate_wave + 1) * carrier_wave


def fm_modulate(carrier_wave: TrigonometricWave, modulate_wave: Wave, k_f=1) -> Wave:
    return CosWave(amplitude=carrier_wave.amplitude, frequency=carrier_wave.frequency,
                   phase=carrier_wave.phase + IntegrateWave(modulate_wave) * k_f)


def pm_modulate(carrier_wave: TrigonometricWave, modulate_wave: Wave, k_p=1) -> Wave:
    return CosWave(amplitude=carrier_wave.amplitude, frequency=carrier_wave.frequency,
                   phase=carrier_wave.phase + modulate_wave * k_p)


def save_gif(figure, gif_name, timeline, signal_waves, carrier_waves, modulated_waves):
    ud = UpdateDist(figure, timeline, signal_waves, carrier_waves, modulated_waves)
    figure.show()
    ani = animation.FuncAnimation(fig=figure, func=ud, frames=20, interval=10, blit=True)
    ani.save(gif_name, writer='pillow')


if __name__ == '__main__':
    time = np.linspace(0, 4, 1000)
    signal = SinWave(amplitude=1, frequency=0.8, phase=0)
    signal += SinWave(amplitude=1, frequency=1, phase=0)
    # signal = SquareWave(signal)
    carrier = CosWave(amplitude=2, frequency=10, phase=0)

    am_modulated = am_modulate(carrier, signal)
    fm_modulated = fm_modulate(carrier, signal, 10)
    pm_modulated = pm_modulate(carrier, signal)
    noise = GaussianNoise(0, 0.5)

    signal_power = np.sum(signal(time) ** 2) / len(time)
    carrier_power = np.sum(carrier(time) ** 2) / len(time)
    am_modulated_power = np.sum(am_modulated(time) ** 2) / len(time)
    fm_modulated_power = np.sum(fm_modulated(time) ** 2) / len(time)
    pm_modulated_power = np.sum(pm_modulated(time) ** 2) / len(time)
    print(f'signal power: {signal_power}')
    print(f'carrier power: {carrier_power}')
    print(f'am modulated power: {am_modulated_power}')
    print(f'fm modulated power: {fm_modulated_power}')
    print(f'pm modulated power: {pm_modulated_power}')
    save_gif(plt.figure(), 'am.gif', time, signal, carrier, am_modulated)
    save_gif(plt.figure(), 'fm.gif', time, signal, carrier, fm_modulated)
    save_gif(plt.figure(), 'pm.gif', time, signal, carrier, pm_modulated)

    save_gif(plt.figure(), 'signal_noise.gif', time, signal, carrier, signal + noise)
    save_gif(plt.figure(), 'am_noise.gif', time, signal, carrier, am_modulated + noise)
    save_gif(plt.figure(), 'fm_noise.gif', time, signal, carrier, fm_modulated + noise)
    save_gif(plt.figure(), 'pm_noise.gif', time, signal, carrier, pm_modulated + noise)
