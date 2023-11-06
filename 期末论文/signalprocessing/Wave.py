from __future__ import annotations
import numpy as np
import scipy.integrate as integrate


class Wave:
    def __str__(self):
        raise NotImplementedError

    def __call__(self, t):
        raise NotImplementedError

    def __add__(self, other) -> Wave:
        if isinstance(other, Wave):
            return MultiWave(self, other)
        elif isinstance(other, (int, float)):
            return MultiWave(self, ConstantWave(other))

    def __radd__(self, other) -> Wave:
        return self + other

    def __mul__(self, other) -> Wave:
        raise NotImplementedError

    def __rmul__(self, other) -> Wave:
        return self * other

    def max_frequency(self):
        raise NotImplementedError

    def max_amplitude(self):
        raise NotImplementedError


class ConstantWave(Wave):
    def __init__(self, amplitude):
        self.amplitude = amplitude

    def __str__(self):
        return f'ConstantWave(Amplitude is {self.amplitude})'

    def __call__(self, t):
        return np.linspace(self.amplitude, self.amplitude, len(t))

    def __mul__(self, other) -> Wave:
        if isinstance(other, (int, float)):
            return ConstantWave(self.amplitude * other)
        elif isinstance(other, Wave):
            return other * self

    def max_frequency(self):
        return 0

    def max_amplitude(self):
        return self.amplitude


class MultiWave(Wave):
    """
    MultiWave is a wave that is the sum of multiple waves
    """
    waves: list[Wave]

    def __init__(self, *waves: Wave):
        self.waves = []
        for wave in waves:
            if isinstance(wave, MultiWave):
                self.waves.extend(wave.waves)
            elif isinstance(wave, Wave):
                self.waves.append(wave)
            else:
                raise TypeError(f'Unsupported type {type(wave)}')

    def __call__(self, t):
        return sum(wave(t) for wave in self.waves)

    def __mul__(self, other):
        return MultiWave(*[wave * other for wave in self.waves])

    def __str__(self):
        return ' + '.join(str(wave) for wave in self.waves)

    def max_frequency(self):
        return max(wave.max_frequency() for wave in self.waves)

    def max_amplitude(self):
        return max(wave.max_amplitude() for wave in self.waves)


class IntegrateWave(Wave):
    """
    IntegrateWave is a wave that is the integral of a wave
    """

    def __init__(self, wave: Wave):
        self.wave = wave

    def __str__(self):
        return f'IntegrateWave({self.wave})'

    def __call__(self, t):
        return integrate.cumtrapz(self.wave(t), t, initial=0)

    def __mul__(self, other):
        """
        only support multiply by a constant
        """
        if isinstance(other, (int, float)):
            return IntegrateWave(self.wave * other)


class TrigonometricWave(Wave):
    """
    TrigonometricWave is a wave that is a trigonometric function
    """

    def __init__(self, amplitude, frequency, phase, info):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.info = info

    def __str__(self):
        return f'{self.info}Wave(Amplitude is {self.amplitude},Frequency is {self.frequency},Initial phase is {self.phase})'

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self * ConstantWave(other)
        elif isinstance(other, ConstantWave):
            if isinstance(self, SinWave):
                return SinWave(amplitude=self.amplitude * other.amplitude, frequency=self.frequency, phase=self.phase)
            elif isinstance(self, CosWave):
                return CosWave(amplitude=self.amplitude * other.amplitude, frequency=self.frequency, phase=self.phase)
        elif isinstance(other, TrigonometricWave):
            diff_frequency = self.frequency - other.frequency
            sum_frequency = self.frequency + other.frequency
            diff_phase = self.phase - other.phase
            sum_phase = self.phase + other.phase
            new_amplitude = 0.5 * self.amplitude * other.amplitude
            if isinstance(self, SinWave):
                if isinstance(other, SinWave):
                    # sin*sin
                    return (CosWave(amplitude=-new_amplitude, frequency=sum_frequency, phase=sum_phase) +
                            CosWave(amplitude=new_amplitude, frequency=diff_frequency, phase=diff_phase))
                elif isinstance(other, CosWave):
                    # sin*cos
                    return (SinWave(amplitude=new_amplitude, frequency=sum_frequency, phase=sum_phase) +
                            SinWave(amplitude=new_amplitude, frequency=diff_frequency, phase=diff_phase))
            elif isinstance(self, CosWave):
                if isinstance(other, SinWave):
                    # cos*sin
                    return (CosWave(amplitude=new_amplitude, frequency=sum_frequency, phase=sum_phase) +
                            SinWave(amplitude=-new_amplitude, frequency=diff_frequency, phase=diff_phase))
                elif isinstance(other, CosWave):
                    # cos*cos
                    return (CosWave(amplitude=new_amplitude, frequency=sum_frequency, phase=sum_phase) +
                            CosWave(amplitude=new_amplitude, frequency=diff_frequency, phase=diff_phase))

    def max_frequency(self):
        return self.frequency

    def max_amplitude(self):
        return self.amplitude


class SquareWave(Wave):
    """
    SquareWave is a wave that is a square wave
    """

    def __init__(self, wave: Wave):
        self.wave = wave

    def __call__(self, t):
        return np.sign(self.wave(t))

    def __mul__(self, other):
        if isinstance(other, SquareWave):
            return SquareWave(self * other.wave)
        return SquareWave(self.wave * other)


class ArccosWave(Wave):
    """
    ArccosWave is a wave that is a arccos wave
    """

    def __init__(self, wave: Wave):
        self.wave = wave

    def __str__(self):
        return f'ArccosWave({self.wave})'

    def __call__(self, t):
        return np.arccos(self.wave(t))


class ArcsinWave(Wave):
    """
    ArcsinWave is a wave that is a arcsin wave
    """

    def __init__(self, wave: Wave):
        self.wave = wave

    def __str__(self):
        return f'ArcsinWave({self.wave})'

    def __call__(self, t):
        return np.arcsin(self.wave(t))


class SinWave(TrigonometricWave):
    def __init__(self, amplitude, frequency, phase):
        super().__init__(amplitude=amplitude, frequency=frequency, phase=phase, info='Sin')

    def __call__(self, t):
        _amplitude = self.amplitude(t) if callable(self.amplitude) else self.amplitude
        _frequency = self.frequency(t) if callable(self.frequency) else self.frequency
        _phase = self.phase(t) if callable(self.phase) else self.phase
        return _amplitude * np.sin(2 * np.pi * _frequency * t + _phase)


class CosWave(TrigonometricWave):
    def __init__(self, amplitude, frequency, phase):
        super().__init__(amplitude=amplitude, frequency=frequency, phase=phase, info='Cos')

    def __call__(self, t):
        _amplitude = self.amplitude(t) if callable(self.amplitude) else self.amplitude
        _frequency = self.frequency(t) if callable(self.frequency) else self.frequency
        _phase = self.phase(t) if callable(self.phase) else self.phase
        return _amplitude * np.cos(2 * np.pi * _frequency * t + _phase)


class GaussianNoise(Wave):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, t):
        return np.random.normal(self.mean, self.std, len(t))

    def __mul__(self, other):
        if isinstance(other, Wave):
            return MultiWave(self, other)
        elif isinstance(other, (int, float)):
            return MultiWave(self, ConstantWave(other))

    def __str__(self):
        return f'GaussianNoise(mean is {self.mean}, std is {self.std})'

    def max_frequency(self):
        return 0

    def max_amplitude(self):
        return self.std
