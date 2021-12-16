import numpy as np


def euler(func, state, time, timestep):
    return state + func(state, time)*timestep


def predict_correct(func, state, time, timestep):
    current_state = state
    state = eiler(func, state, time, timestep)
    return current_state + func(state, time)*timestep


def hune(func, state, time, timestep):
    current_state = state
    state = euler(func, state, time, timestep)
    return ((current_state + func(state, time) * timestep) + state) * 0.5


def integrator_method(next_step, func, initial_state, initial_time, timestep, n_iters):
    """
    :param next_step: function determine method
    :param func: function determine physical model
    :param initial_state: initial state of system (Koshы problem)
    :param timestep: time step
    :param n_iters: amount of iterations
    :return: sequence of approximations of system's state
    """
    result = []

    state = initial_state
    time = initial_time

    result.append(state)

    for i in range(n_iters):
        state = next_step(func, state, time, timestep)
        time += timestep
        result.append(state)
    return np.array(result)


if __name__ == '__main__':
    print('Make sure you do all right')
